import warnings
from logging import getLogger
from scrapy import signals
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.http import Response, TextResponse
from scrapy.responsetypes import responsetypes
from scrapy.utils._compression import _DecompressionMaxSizeExceeded, _inflate, _unbrotli, _unzstd
from scrapy.utils.deprecate import ScrapyDeprecationWarning
from scrapy.utils.gz import gunzip
logger = getLogger(__name__)
ACCEPTED_ENCODINGS = [b'gzip', b'deflate']
try:
    import brotli
except ImportError:
    pass
else:
    ACCEPTED_ENCODINGS.append(b'br')
try:
    import zstandard
except ImportError:
    pass
else:
    ACCEPTED_ENCODINGS.append(b'zstd')

class HttpCompressionMiddleware:
    """This middleware allows compressed (gzip, deflate) traffic to be
    sent/received from web sites"""

    def __init__(self, stats=None, *, crawler=None):
        if not crawler:
            self.stats = stats
            self._max_size = 1073741824
            self._warn_size = 33554432
            return
        self.stats = crawler.stats
        self._max_size = crawler.settings.getint('DOWNLOAD_MAXSIZE')
        self._warn_size = crawler.settings.getint('DOWNLOAD_WARNSIZE')
        crawler.signals.connect(self.open_spider, signals.spider_opened)