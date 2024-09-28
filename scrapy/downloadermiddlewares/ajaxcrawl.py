import logging
import re
from w3lib import html
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse
logger = logging.getLogger(__name__)

class AjaxCrawlMiddleware:
    """
    Handle 'AJAX crawlable' pages marked as crawlable via meta tag.
    For more info see https://developers.google.com/webmasters/ajax-crawling/docs/getting-started.
    """

    def __init__(self, settings):
        if not settings.getbool('AJAXCRAWL_ENABLED'):
            raise NotConfigured
        self.lookup_bytes = settings.getint('AJAXCRAWL_MAXSIZE', 32768)

    def _has_ajax_crawlable_variant(self, response):
        """
        Return True if a page without hash fragment could be "AJAX crawlable"
        according to https://developers.google.com/webmasters/ajax-crawling/docs/getting-started.
        """
        pass
_ajax_crawlable_re = re.compile('<meta\\s+name=["\\\']fragment["\\\']\\s+content=["\\\']!["\\\']/?>')

def _has_ajaxcrawlable_meta(text):
    """
    >>> _has_ajaxcrawlable_meta('<html><head><meta name="fragment"  content="!"/></head><body></body></html>')
    True
    >>> _has_ajaxcrawlable_meta("<html><head><meta name='fragment' content='!'></head></html>")
    True
    >>> _has_ajaxcrawlable_meta('<html><head><!--<meta name="fragment"  content="!"/>--></head><body></body></html>')
    False
    >>> _has_ajaxcrawlable_meta('<html></html>')
    False
    """
    pass