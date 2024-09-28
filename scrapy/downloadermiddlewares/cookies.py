import logging
from collections import defaultdict
from tldextract import TLDExtract
from scrapy.exceptions import NotConfigured
from scrapy.http import Response
from scrapy.http.cookies import CookieJar
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.python import to_unicode
logger = logging.getLogger(__name__)
_split_domain = TLDExtract(include_psl_private_domains=True)

class CookiesMiddleware:
    """This middleware enables working with sites that need cookies"""

    def __init__(self, debug=False):
        self.jars = defaultdict(CookieJar)
        self.debug = debug

    def _format_cookie(self, cookie, request):
        """
        Given a dict consisting of cookie components, return its string representation.
        Decode from bytes if necessary.
        """
        pass

    def _get_request_cookies(self, jar, request):
        """
        Extract cookies from the Request.cookies attribute
        """
        pass