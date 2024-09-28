import base64
from urllib.parse import unquote, urlunparse
from urllib.request import _parse_proxy, getproxies, proxy_bypass
from scrapy.exceptions import NotConfigured
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.python import to_bytes

class HttpProxyMiddleware:

    def __init__(self, auth_encoding='latin-1'):
        self.auth_encoding = auth_encoding
        self.proxies = {}
        for type_, url in getproxies().items():
            try:
                self.proxies[type_] = self._get_proxy(url, type_)
            except ValueError:
                continue