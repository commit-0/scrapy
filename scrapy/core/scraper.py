"""This module implements the Scraper component which parses responses and
extracts information from them"""
from __future__ import annotations
import logging
from collections import deque
from typing import TYPE_CHECKING, Any, AsyncGenerator, AsyncIterable, Deque, Generator, Iterable, Optional, Set, Tuple, Type, Union
from itemadapter import is_item
from twisted.internet.defer import Deferred, inlineCallbacks
from twisted.python.failure import Failure
from scrapy import Spider, signals
from scrapy.core.spidermw import SpiderMiddlewareManager
from scrapy.exceptions import CloseSpider, DropItem, IgnoreRequest
from scrapy.http import Request, Response
from scrapy.logformatter import LogFormatter
from scrapy.pipelines import ItemPipelineManager
from scrapy.signalmanager import SignalManager
from scrapy.utils.defer import aiter_errback, defer_fail, defer_succeed, iter_errback, parallel, parallel_async
from scrapy.utils.log import failure_to_exc_info, logformatter_adapter
from scrapy.utils.misc import load_object, warn_on_generator_with_return_value
from scrapy.utils.spider import iterate_spider_output
if TYPE_CHECKING:
    from scrapy.crawler import Crawler
QueueTuple = Tuple[Union[Response, Failure], Request, Deferred]
logger = logging.getLogger(__name__)

class Slot:
    """Scraper slot (one per running spider)"""
    MIN_RESPONSE_SIZE = 1024

    def __init__(self, max_active_size: int=5000000):
        self.max_active_size = max_active_size
        self.queue: Deque[QueueTuple] = deque()
        self.active: Set[Request] = set()
        self.active_size: int = 0
        self.itemproc_size: int = 0
        self.closing: Optional[Deferred] = None

class Scraper:

    def __init__(self, crawler: Crawler) -> None:
        self.slot: Optional[Slot] = None
        self.spidermw: SpiderMiddlewareManager = SpiderMiddlewareManager.from_crawler(crawler)
        itemproc_cls: Type[ItemPipelineManager] = load_object(crawler.settings['ITEM_PROCESSOR'])
        self.itemproc: ItemPipelineManager = itemproc_cls.from_crawler(crawler)
        self.concurrent_items: int = crawler.settings.getint('CONCURRENT_ITEMS')
        self.crawler: Crawler = crawler
        self.signals: SignalManager = crawler.signals
        assert crawler.logformatter
        self.logformatter: LogFormatter = crawler.logformatter

    @inlineCallbacks
    def open_spider(self, spider: Spider) -> Generator[Deferred, Any, None]:
        """Open the given spider for scraping and allocate resources for it"""
        pass

    def close_spider(self, spider: Spider) -> Deferred:
        """Close a spider being scraped and release its resources"""
        pass

    def is_idle(self) -> bool:
        """Return True if there isn't any more spiders to process"""
        pass

    def _scrape(self, result: Union[Response, Failure], request: Request, spider: Spider) -> Deferred:
        """
        Handle the downloaded response or failure through the spider callback/errback
        """
        pass

    def _scrape2(self, result: Union[Response, Failure], request: Request, spider: Spider) -> Deferred:
        """
        Handle the different cases of request's result been a Response or a Failure
        """
        pass

    def _process_spidermw_output(self, output: Any, request: Request, response: Response, spider: Spider) -> Optional[Deferred]:
        """Process each Request/Item (given in the output parameter) returned
        from the given spider
        """
        pass

    def _log_download_errors(self, spider_failure: Failure, download_failure: Failure, request: Request, spider: Spider) -> Union[Failure, None]:
        """Log and silence errors that come from the engine (typically download
        errors that got propagated thru here).

        spider_failure: the value passed into the errback of self.call_spider()
        download_failure: the value passed into _scrape2() from
        ExecutionEngine._handle_downloader_output() as "result"
        """
        pass

    def _itemproc_finished(self, output: Any, item: Any, response: Response, spider: Spider) -> Deferred:
        """ItemProcessor finished for the given ``item`` and returned ``output``"""
        pass