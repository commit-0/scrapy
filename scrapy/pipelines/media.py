import functools
import logging
from collections import defaultdict
from inspect import signature
from warnings import warn
from twisted.internet.defer import Deferred, DeferredList
from twisted.python.failure import Failure
from scrapy.http.request import NO_CALLBACK
from scrapy.settings import Settings
from scrapy.utils.datatypes import SequenceExclude
from scrapy.utils.defer import defer_result, mustbe_deferred
from scrapy.utils.deprecate import ScrapyDeprecationWarning
from scrapy.utils.log import failure_to_exc_info
from scrapy.utils.misc import arg_to_iter
logger = logging.getLogger(__name__)

class MediaPipeline:
    LOG_FAILED_RESULTS = True

    class SpiderInfo:

        def __init__(self, spider):
            self.spider = spider
            self.downloading = set()
            self.downloaded = {}
            self.waiting = defaultdict(list)

    def __init__(self, download_func=None, settings=None):
        self.download_func = download_func
        self._expects_item = {}
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)
        resolve = functools.partial(self._key_for_pipe, base_class_name='MediaPipeline', settings=settings)
        self.allow_redirects = settings.getbool(resolve('MEDIA_ALLOW_REDIRECTS'), False)
        self._handle_statuses(self.allow_redirects)
        self._make_compatible()

    def _key_for_pipe(self, key, base_class_name=None, settings=None):
        """
        >>> MediaPipeline()._key_for_pipe("IMAGES")
        'IMAGES'
        >>> class MyPipe(MediaPipeline):
        ...     pass
        >>> MyPipe()._key_for_pipe("IMAGES", base_class_name="MediaPipeline")
        'MYPIPE_IMAGES'
        """
        pass

    def _make_compatible(self):
        """Make overridable methods of MediaPipeline and subclasses backwards compatible"""
        pass

    def _compatible(self, func):
        """Wrapper for overridable methods to allow backwards compatibility"""
        pass

    def media_to_download(self, request, info, *, item=None):
        """Check request before starting download"""
        pass

    def get_media_requests(self, item, info):
        """Returns the media requests to download"""
        pass

    def media_downloaded(self, response, request, info, *, item=None):
        """Handler for success downloads"""
        pass

    def media_failed(self, failure, request, info):
        """Handler for failed downloads"""
        pass

    def item_completed(self, results, item, info):
        """Called per item when all media requests has been processed"""
        pass

    def file_path(self, request, response=None, info=None, *, item=None):
        """Returns the path where downloaded media should be stored"""
        pass