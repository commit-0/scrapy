from collections import deque
from typing import Deque, Dict, List, Optional, Tuple
from twisted.internet import defer
from twisted.internet.base import ReactorBase
from twisted.internet.defer import Deferred
from twisted.internet.endpoints import HostnameEndpoint
from twisted.python.failure import Failure
from twisted.web.client import URI, BrowserLikePolicyForHTTPS, ResponseFailed, _StandardEndpointFactory
from twisted.web.error import SchemeNotSupported
from scrapy.core.downloader.contextfactory import AcceptableProtocolsContextFactory
from scrapy.core.http2.protocol import H2ClientFactory, H2ClientProtocol
from scrapy.http.request import Request
from scrapy.settings import Settings
from scrapy.spiders import Spider

class H2ConnectionPool:

    def __init__(self, reactor: ReactorBase, settings: Settings) -> None:
        self._reactor = reactor
        self.settings = settings
        self._connections: Dict[Tuple, H2ClientProtocol] = {}
        self._pending_requests: Dict[Tuple, Deque[Deferred]] = {}

    def close_connections(self) -> None:
        """Close all the HTTP/2 connections and remove them from pool

        Returns:
            Deferred that fires when all connections have been closed
        """
        pass

class H2Agent:

    def __init__(self, reactor: ReactorBase, pool: H2ConnectionPool, context_factory: BrowserLikePolicyForHTTPS=BrowserLikePolicyForHTTPS(), connect_timeout: Optional[float]=None, bind_address: Optional[bytes]=None) -> None:
        self._reactor = reactor
        self._pool = pool
        self._context_factory = AcceptableProtocolsContextFactory(context_factory, acceptable_protocols=[b'h2'])
        self.endpoint_factory = _StandardEndpointFactory(self._reactor, self._context_factory, connect_timeout, bind_address)

    def get_key(self, uri: URI) -> Tuple:
        """
        Arguments:
            uri - URI obtained directly from request URL
        """
        pass

class ScrapyProxyH2Agent(H2Agent):

    def __init__(self, reactor: ReactorBase, proxy_uri: URI, pool: H2ConnectionPool, context_factory: BrowserLikePolicyForHTTPS=BrowserLikePolicyForHTTPS(), connect_timeout: Optional[float]=None, bind_address: Optional[bytes]=None) -> None:
        super().__init__(reactor=reactor, pool=pool, context_factory=context_factory, connect_timeout=connect_timeout, bind_address=bind_address)
        self._proxy_uri = proxy_uri

    def get_key(self, uri: URI) -> Tuple:
        """We use the proxy uri instead of uri obtained from request url"""
        pass