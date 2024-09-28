from email.utils import formatdate
from typing import Optional, Type, TypeVar
from twisted.internet import defer
from twisted.internet.error import ConnectError, ConnectionDone, ConnectionLost, ConnectionRefusedError, DNSLookupError, TCPTimedOutError, TimeoutError
from twisted.web.client import ResponseFailed
from scrapy import signals
from scrapy.crawler import Crawler
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.http.request import Request
from scrapy.http.response import Response
from scrapy.settings import Settings
from scrapy.spiders import Spider
from scrapy.statscollectors import StatsCollector
from scrapy.utils.misc import load_object
HttpCacheMiddlewareTV = TypeVar('HttpCacheMiddlewareTV', bound='HttpCacheMiddleware')

class HttpCacheMiddleware:
    DOWNLOAD_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError, ConnectionRefusedError, ConnectionDone, ConnectError, ConnectionLost, TCPTimedOutError, ResponseFailed, OSError)

    def __init__(self, settings: Settings, stats: StatsCollector) -> None:
        if not settings.getbool('HTTPCACHE_ENABLED'):
            raise NotConfigured
        self.policy = load_object(settings['HTTPCACHE_POLICY'])(settings)
        self.storage = load_object(settings['HTTPCACHE_STORAGE'])(settings)
        self.ignore_missing = settings.getbool('HTTPCACHE_IGNORE_MISSING')
        self.stats = stats