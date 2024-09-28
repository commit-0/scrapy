"""
Files Pipeline

See documentation in topics/media-pipeline.rst
"""
import base64
import functools
import hashlib
import logging
import mimetypes
import os
import time
from collections import defaultdict
from contextlib import suppress
from ftplib import FTP
from io import BytesIO
from os import PathLike
from pathlib import Path
from typing import DefaultDict, Optional, Set, Union
from urllib.parse import urlparse
from itemadapter import ItemAdapter
from twisted.internet import defer, threads
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.http import Request
from scrapy.http.request import NO_CALLBACK
from scrapy.pipelines.media import MediaPipeline
from scrapy.settings import Settings
from scrapy.utils.boto import is_botocore_available
from scrapy.utils.datatypes import CaseInsensitiveDict
from scrapy.utils.ftp import ftp_store_file
from scrapy.utils.log import failure_to_exc_info
from scrapy.utils.misc import md5sum
from scrapy.utils.python import to_bytes
from scrapy.utils.request import referer_str
logger = logging.getLogger(__name__)

class FileException(Exception):
    """General media error exception"""

class FSFilesStore:

    def __init__(self, basedir: Union[str, PathLike]):
        basedir = _to_string(basedir)
        if '://' in basedir:
            basedir = basedir.split('://', 1)[1]
        self.basedir = basedir
        self._mkdir(Path(self.basedir))
        self.created_directories: DefaultDict[str, Set[str]] = defaultdict(set)

class S3FilesStore:
    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None
    AWS_SESSION_TOKEN = None
    AWS_ENDPOINT_URL = None
    AWS_REGION_NAME = None
    AWS_USE_SSL = None
    AWS_VERIFY = None
    POLICY = 'private'
    HEADERS = {'Cache-Control': 'max-age=172800'}

    def __init__(self, uri):
        if not is_botocore_available():
            raise NotConfigured('missing botocore library')
        import botocore.session
        session = botocore.session.get_session()
        self.s3_client = session.create_client('s3', aws_access_key_id=self.AWS_ACCESS_KEY_ID, aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY, aws_session_token=self.AWS_SESSION_TOKEN, endpoint_url=self.AWS_ENDPOINT_URL, region_name=self.AWS_REGION_NAME, use_ssl=self.AWS_USE_SSL, verify=self.AWS_VERIFY)
        if not uri.startswith('s3://'):
            raise ValueError(f"Incorrect URI scheme in {uri}, expected 's3'")
        self.bucket, self.prefix = uri[5:].split('/', 1)

    def persist_file(self, path, buf, info, meta=None, headers=None):
        """Upload file to S3 storage"""
        pass

    def _headers_to_botocore_kwargs(self, headers):
        """Convert headers to botocore keyword arguments."""
        pass

class GCSFilesStore:
    GCS_PROJECT_ID = None
    CACHE_CONTROL = 'max-age=172800'
    POLICY = None

    def __init__(self, uri):
        from google.cloud import storage
        client = storage.Client(project=self.GCS_PROJECT_ID)
        bucket, prefix = uri[5:].split('/', 1)
        self.bucket = client.bucket(bucket)
        self.prefix = prefix
        permissions = self.bucket.test_iam_permissions(['storage.objects.get', 'storage.objects.create'])
        if 'storage.objects.get' not in permissions:
            logger.warning("No 'storage.objects.get' permission for GSC bucket %(bucket)s. Checking if files are up to date will be impossible. Files will be downloaded every time.", {'bucket': bucket})
        if 'storage.objects.create' not in permissions:
            logger.error("No 'storage.objects.create' permission for GSC bucket %(bucket)s. Saving files will be impossible!", {'bucket': bucket})

class FTPFilesStore:
    FTP_USERNAME = None
    FTP_PASSWORD = None
    USE_ACTIVE_MODE = None

    def __init__(self, uri):
        if not uri.startswith('ftp://'):
            raise ValueError(f"Incorrect URI scheme in {uri}, expected 'ftp'")
        u = urlparse(uri)
        self.port = u.port
        self.host = u.hostname
        self.port = int(u.port or 21)
        self.username = u.username or self.FTP_USERNAME
        self.password = u.password or self.FTP_PASSWORD
        self.basedir = u.path.rstrip('/')

class FilesPipeline(MediaPipeline):
    """Abstract pipeline that implement the file downloading

    This pipeline tries to minimize network transfers and file processing,
    doing stat of the files and determining if file is new, up-to-date or
    expired.

    ``new`` files are those that pipeline never processed and needs to be
        downloaded from supplier site the first time.

    ``uptodate`` files are the ones that the pipeline processed and are still
        valid files.

    ``expired`` files are those that pipeline already processed but the last
        modification was made long time ago, so a reprocessing is recommended to
        refresh it in case of change.

    """
    MEDIA_NAME = 'file'
    EXPIRES = 90
    STORE_SCHEMES = {'': FSFilesStore, 'file': FSFilesStore, 's3': S3FilesStore, 'gs': GCSFilesStore, 'ftp': FTPFilesStore}
    DEFAULT_FILES_URLS_FIELD = 'file_urls'
    DEFAULT_FILES_RESULT_FIELD = 'files'

    def __init__(self, store_uri, download_func=None, settings=None):
        store_uri = _to_string(store_uri)
        if not store_uri:
            raise NotConfigured
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)
        cls_name = 'FilesPipeline'
        self.store = self._get_store(store_uri)
        resolve = functools.partial(self._key_for_pipe, base_class_name=cls_name, settings=settings)
        self.expires = settings.getint(resolve('FILES_EXPIRES'), self.EXPIRES)
        if not hasattr(self, 'FILES_URLS_FIELD'):
            self.FILES_URLS_FIELD = self.DEFAULT_FILES_URLS_FIELD
        if not hasattr(self, 'FILES_RESULT_FIELD'):
            self.FILES_RESULT_FIELD = self.DEFAULT_FILES_RESULT_FIELD
        self.files_urls_field = settings.get(resolve('FILES_URLS_FIELD'), self.FILES_URLS_FIELD)
        self.files_result_field = settings.get(resolve('FILES_RESULT_FIELD'), self.FILES_RESULT_FIELD)
        super().__init__(download_func=download_func, settings=settings)