"""
This is a middleware to respect robots.txt policies. To activate it you must
enable this middleware and enable the ROBOTSTXT_OBEY setting.

"""
import logging
from twisted.internet.defer import Deferred, maybeDeferred
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.http import Request
from scrapy.http.request import NO_CALLBACK
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.log import failure_to_exc_info
from scrapy.utils.misc import load_object
logger = logging.getLogger(__name__)

class RobotsTxtMiddleware:
    DOWNLOAD_PRIORITY = 1000

    def __init__(self, crawler):
        if not crawler.settings.getbool('ROBOTSTXT_OBEY'):
            raise NotConfigured
        self._default_useragent = crawler.settings.get('USER_AGENT', 'Scrapy')
        self._robotstxt_useragent = crawler.settings.get('ROBOTSTXT_USER_AGENT', None)
        self.crawler = crawler
        self._parsers = {}
        self._parserimpl = load_object(crawler.settings.get('ROBOTSTXT_PARSER'))
        self._parserimpl.from_crawler(self.crawler, b'')