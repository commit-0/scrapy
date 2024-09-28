import re
from time import time
from typing import Optional, Tuple
from urllib.parse import ParseResult, urldefrag, urlparse, urlunparse
from twisted.internet import defer
from twisted.internet.protocol import ClientFactory
from twisted.web.http import HTTPClient
from scrapy import Request
from scrapy.http import Headers
from scrapy.responsetypes import responsetypes
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.python import to_bytes, to_unicode

def _parse(url: str) -> Tuple[bytes, bytes, bytes, int, bytes]:
    """Return tuple of (scheme, netloc, host, port, path),
    all in bytes except for port which is int.
    Assume url is from Request.url, which was passed via safe_url_string
    and is ascii-only.
    """
    pass

class ScrapyHTTPPageGetter(HTTPClient):
    delimiter = b'\n'

class ScrapyHTTPClientFactory(ClientFactory):
    protocol = ScrapyHTTPPageGetter
    waiting = 1
    noisy = False
    followRedirect = False
    afterFoundGet = False

    def __init__(self, request: Request, timeout: float=180):
        self._url: str = urldefrag(request.url)[0]
        self.url: bytes = to_bytes(self._url, encoding='ascii')
        self.method: bytes = to_bytes(request.method, encoding='ascii')
        self.body: Optional[bytes] = request.body or None
        self.headers: Headers = Headers(request.headers)
        self.response_headers: Optional[Headers] = None
        self.timeout: float = request.meta.get('download_timeout') or timeout
        self.start_time: float = time()
        self.deferred: defer.Deferred = defer.Deferred().addCallback(self._build_response, request)
        self._disconnectedDeferred: defer.Deferred = defer.Deferred()
        self._set_connection_attributes(request)
        self.headers.setdefault('Host', self.netloc)
        if self.body is not None:
            self.headers['Content-Length'] = len(self.body)
            self.headers.setdefault('Connection', 'close')
        elif self.method == b'POST':
            self.headers['Content-Length'] = 0

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self._url}>'

    def gotStatus(self, version, status, message):
        """
        Set the status of the request on us.
        @param version: The HTTP version.
        @type version: L{bytes}
        @param status: The HTTP status code, an integer represented as a
        bytestring.
        @type status: L{bytes}
        @param message: The HTTP status message.
        @type message: L{bytes}
        """
        pass

    def clientConnectionFailed(self, _, reason):
        """
        When a connection attempt fails, the request cannot be issued.  If no
        result has yet been provided to the result Deferred, provide the
        connection failure reason as an error result.
        """
        pass