"""CloseSpider is an extension that forces spiders to be closed after certain
conditions are met.

See documentation in docs/topics/extensions.rst
"""
import logging
from collections import defaultdict
from scrapy import signals
from scrapy.exceptions import NotConfigured
logger = logging.getLogger(__name__)

class CloseSpider:

    def __init__(self, crawler):
        self.crawler = crawler
        self.close_on = {'timeout': crawler.settings.getfloat('CLOSESPIDER_TIMEOUT'), 'itemcount': crawler.settings.getint('CLOSESPIDER_ITEMCOUNT'), 'pagecount': crawler.settings.getint('CLOSESPIDER_PAGECOUNT'), 'errorcount': crawler.settings.getint('CLOSESPIDER_ERRORCOUNT'), 'timeout_no_item': crawler.settings.getint('CLOSESPIDER_TIMEOUT_NO_ITEM')}
        if not any(self.close_on.values()):
            raise NotConfigured
        self.counter = defaultdict(int)
        if self.close_on.get('errorcount'):
            crawler.signals.connect(self.error_count, signal=signals.spider_error)
        if self.close_on.get('pagecount'):
            crawler.signals.connect(self.page_count, signal=signals.response_received)
        if self.close_on.get('timeout'):
            crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
        if self.close_on.get('itemcount'):
            crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
        if self.close_on.get('timeout_no_item'):
            self.timeout_no_item = self.close_on['timeout_no_item']
            self.items_in_period = 0
            crawler.signals.connect(self.spider_opened_no_item, signal=signals.spider_opened)
            crawler.signals.connect(self.item_scraped_no_item, signal=signals.item_scraped)
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)