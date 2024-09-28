from time import time
from typing import Optional, Type, TypeVar
from urllib.parse import urldefrag
from twisted.internet.base import DelayedCall
from twisted.internet.defer import Deferred
from twisted.internet.error import TimeoutError
from twisted.web.client import URI
from scrapy.core.downloader.contextfactory import load_context_factory_from_settings
from scrapy.core.downloader.webclient import _parse
from scrapy.core.http2.agent import H2Agent, H2ConnectionPool, ScrapyProxyH2Agent
from scrapy.crawler import Crawler
from scrapy.http import Request, Response
from scrapy.settings import Settings
from scrapy.spiders import Spider
from scrapy.utils.python import to_bytes
H2DownloadHandlerOrSubclass = TypeVar('H2DownloadHandlerOrSubclass', bound='H2DownloadHandler')

class H2DownloadHandler:

    def __init__(self, settings: Settings, crawler: Optional[Crawler]=None):
        self._crawler = crawler
        from twisted.internet import reactor
        self._pool = H2ConnectionPool(reactor, settings)
        self._context_factory = load_context_factory_from_settings(settings, crawler)

class ScrapyH2Agent:
    _Agent = H2Agent
    _ProxyAgent = ScrapyProxyH2Agent

    def __init__(self, context_factory, pool: H2ConnectionPool, connect_timeout: int=10, bind_address: Optional[bytes]=None, crawler: Optional[Crawler]=None) -> None:
        self._context_factory = context_factory
        self._connect_timeout = connect_timeout
        self._bind_address = bind_address
        self._pool = pool
        self._crawler = crawler