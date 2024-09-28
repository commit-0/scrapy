"""
Feed Exports extension

See documentation in docs/topics/feed-exports.rst
"""
import logging
import re
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path, PureWindowsPath
from tempfile import NamedTemporaryFile
from typing import IO, Any, Callable, Dict, List, Optional, Tuple, Union
from urllib.parse import unquote, urlparse
from twisted.internet import defer, threads
from twisted.internet.defer import DeferredList
from w3lib.url import file_uri_to_path
from zope.interface import Interface, implementer
from scrapy import Spider, signals
from scrapy.exceptions import NotConfigured, ScrapyDeprecationWarning
from scrapy.extensions.postprocessing import PostProcessingManager
from scrapy.utils.boto import is_botocore_available
from scrapy.utils.conf import feed_complete_default_values_from_settings
from scrapy.utils.defer import maybe_deferred_to_future
from scrapy.utils.deprecate import create_deprecated_class
from scrapy.utils.ftp import ftp_store_file
from scrapy.utils.log import failure_to_exc_info
from scrapy.utils.misc import create_instance, load_object
from scrapy.utils.python import get_func_args, without_none_values
logger = logging.getLogger(__name__)
try:
    import boto3
    IS_BOTO3_AVAILABLE = True
except ImportError:
    IS_BOTO3_AVAILABLE = False

class ItemFilter:
    """
    This will be used by FeedExporter to decide if an item should be allowed
    to be exported to a particular feed.

    :param feed_options: feed specific options passed from FeedExporter
    :type feed_options: dict
    """
    feed_options: Optional[dict]
    item_classes: Tuple

    def __init__(self, feed_options: Optional[dict]) -> None:
        self.feed_options = feed_options
        if feed_options is not None:
            self.item_classes = tuple((load_object(item_class) for item_class in feed_options.get('item_classes') or ()))
        else:
            self.item_classes = tuple()

    def accepts(self, item: Any) -> bool:
        """
        Return ``True`` if `item` should be exported or ``False`` otherwise.

        :param item: scraped item which user wants to check if is acceptable
        :type item: :ref:`Scrapy items <topics-items>`
        :return: `True` if accepted, `False` otherwise
        :rtype: bool
        """
        pass

class IFeedStorage(Interface):
    """Interface that all Feed Storages must implement"""

    def __init__(uri, *, feed_options=None):
        """Initialize the storage with the parameters given in the URI and the
        feed-specific options (see :setting:`FEEDS`)"""

    def open(spider):
        """Open the storage for the given spider. It must return a file-like
        object that will be used for the exporters"""
        pass

    def store(file):
        """Store the given file stream"""
        pass

@implementer(IFeedStorage)
class BlockingFeedStorage:
    pass

@implementer(IFeedStorage)
class StdoutFeedStorage:

    def __init__(self, uri, _stdout=None, *, feed_options=None):
        if not _stdout:
            _stdout = sys.stdout.buffer
        self._stdout = _stdout
        if feed_options and feed_options.get('overwrite', False) is True:
            logger.warning('Standard output (stdout) storage does not support overwriting. To suppress this warning, remove the overwrite option from your FEEDS setting, or set it to False.')

@implementer(IFeedStorage)
class FileFeedStorage:

    def __init__(self, uri, *, feed_options=None):
        self.path = file_uri_to_path(uri)
        feed_options = feed_options or {}
        self.write_mode = 'wb' if feed_options.get('overwrite', False) else 'ab'

class S3FeedStorage(BlockingFeedStorage):

    def __init__(self, uri, access_key=None, secret_key=None, acl=None, endpoint_url=None, *, feed_options=None, session_token=None, region_name=None):
        if not is_botocore_available():
            raise NotConfigured('missing botocore library')
        u = urlparse(uri)
        self.bucketname = u.hostname
        self.access_key = u.username or access_key
        self.secret_key = u.password or secret_key
        self.session_token = session_token
        self.keyname = u.path[1:]
        self.acl = acl
        self.endpoint_url = endpoint_url
        self.region_name = region_name
        if IS_BOTO3_AVAILABLE:
            import boto3.session
            session = boto3.session.Session()
            self.s3_client = session.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key, aws_session_token=self.session_token, endpoint_url=self.endpoint_url, region_name=self.region_name)
        else:
            warnings.warn('`botocore` usage has been deprecated for S3 feed export, please use `boto3` to avoid problems', category=ScrapyDeprecationWarning)
            import botocore.session
            session = botocore.session.get_session()
            self.s3_client = session.create_client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key, aws_session_token=self.session_token, endpoint_url=self.endpoint_url, region_name=self.region_name)
        if feed_options and feed_options.get('overwrite', True) is False:
            logger.warning('S3 does not support appending to files. To suppress this warning, remove the overwrite option from your FEEDS setting or set it to True.')

class GCSFeedStorage(BlockingFeedStorage):

    def __init__(self, uri, project_id, acl):
        self.project_id = project_id
        self.acl = acl
        u = urlparse(uri)
        self.bucket_name = u.hostname
        self.blob_name = u.path[1:]

class FTPFeedStorage(BlockingFeedStorage):

    def __init__(self, uri: str, use_active_mode: bool=False, *, feed_options: Optional[Dict[str, Any]]=None):
        u = urlparse(uri)
        if not u.hostname:
            raise ValueError(f'Got a storage URI without a hostname: {uri}')
        self.host: str = u.hostname
        self.port: int = int(u.port or '21')
        self.username: str = u.username or ''
        self.password: str = unquote(u.password or '')
        self.path: str = u.path
        self.use_active_mode: bool = use_active_mode
        self.overwrite: bool = not feed_options or feed_options.get('overwrite', True)

class FeedSlot:

    def __init__(self, storage, uri, format, store_empty, batch_id, uri_template, filter, feed_options, spider, exporters, settings, crawler):
        self.file = None
        self.exporter = None
        self.storage = storage
        self.batch_id = batch_id
        self.format = format
        self.store_empty = store_empty
        self.uri_template = uri_template
        self.uri = uri
        self.filter = filter
        self.feed_options = feed_options
        self.spider = spider
        self.exporters = exporters
        self.settings = settings
        self.crawler = crawler
        self.itemcount = 0
        self._exporting = False
        self._fileloaded = False
_FeedSlot = create_deprecated_class(name='_FeedSlot', new_class=FeedSlot)

class FeedExporter:
    _pending_deferreds: List[defer.Deferred] = []

    def __init__(self, crawler):
        self.crawler = crawler
        self.settings = crawler.settings
        self.feeds = {}
        self.slots = []
        self.filters = {}
        if not self.settings['FEEDS'] and (not self.settings['FEED_URI']):
            raise NotConfigured
        if self.settings['FEED_URI']:
            warnings.warn('The `FEED_URI` and `FEED_FORMAT` settings have been deprecated in favor of the `FEEDS` setting. Please see the `FEEDS` setting docs for more details', category=ScrapyDeprecationWarning, stacklevel=2)
            uri = self.settings['FEED_URI']
            uri = str(uri) if not isinstance(uri, Path) else uri.absolute().as_uri()
            feed_options = {'format': self.settings.get('FEED_FORMAT', 'jsonlines')}
            self.feeds[uri] = feed_complete_default_values_from_settings(feed_options, self.settings)
            self.filters[uri] = self._load_filter(feed_options)
        for uri, feed_options in self.settings.getdict('FEEDS').items():
            uri = str(uri) if not isinstance(uri, Path) else uri.absolute().as_uri()
            self.feeds[uri] = feed_complete_default_values_from_settings(feed_options, self.settings)
            self.filters[uri] = self._load_filter(feed_options)
        self.storages = self._load_components('FEED_STORAGES')
        self.exporters = self._load_components('FEED_EXPORTERS')
        for uri, feed_options in self.feeds.items():
            if not self._storage_supported(uri, feed_options):
                raise NotConfigured
            if not self._settings_are_valid():
                raise NotConfigured
            if not self._exporter_supported(feed_options['format']):
                raise NotConfigured

    def _start_new_batch(self, batch_id, uri, feed_options, spider, uri_template):
        """
        Redirect the output data stream to a new file.
        Execute multiple times if FEED_EXPORT_BATCH_ITEM_COUNT setting or FEEDS.batch_item_count is specified
        :param batch_id: sequence number of current batch
        :param uri: uri of the new batch to start
        :param feed_options: dict with parameters of feed
        :param spider: user spider
        :param uri_template: template of uri which contains %(batch_time)s or %(batch_id)d to create new uri
        """
        pass

    def _settings_are_valid(self):
        """
        If FEED_EXPORT_BATCH_ITEM_COUNT setting or FEEDS.batch_item_count is specified uri has to contain
        %(batch_time)s or %(batch_id)d to distinguish different files of partial output
        """
        pass

    def _get_storage(self, uri, feed_options):
        """Fork of create_instance specific to feed storage classes

        It supports not passing the *feed_options* parameters to classes that
        do not support it, and issuing a deprecation warning instead.
        """
        pass