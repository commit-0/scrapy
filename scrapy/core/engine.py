"""
This is the Scrapy engine which controls the Scheduler, Downloader and Spider.

For more information see docs/topics/architecture.rst

"""
import logging
from time import time
from typing import TYPE_CHECKING, Any, Callable, Generator, Iterable, Iterator, Optional, Set, Type, Union, cast
from twisted.internet.defer import Deferred, inlineCallbacks, succeed
from twisted.internet.task import LoopingCall
from twisted.python.failure import Failure
from scrapy import signals
from scrapy.core.downloader import Downloader
from scrapy.core.scraper import Scraper
from scrapy.exceptions import CloseSpider, DontCloseSpider, IgnoreRequest
from scrapy.http import Request, Response
from scrapy.logformatter import LogFormatter
from scrapy.settings import BaseSettings, Settings
from scrapy.signalmanager import SignalManager
from scrapy.spiders import Spider
from scrapy.utils.log import failure_to_exc_info, logformatter_adapter
from scrapy.utils.misc import create_instance, load_object
from scrapy.utils.python import global_object_name
from scrapy.utils.reactor import CallLaterOnce
if TYPE_CHECKING:
    from scrapy.core.scheduler import BaseScheduler
    from scrapy.crawler import Crawler
logger = logging.getLogger(__name__)

class Slot:

    def __init__(self, start_requests: Iterable[Request], close_if_idle: bool, nextcall: CallLaterOnce, scheduler: 'BaseScheduler') -> None:
        self.closing: Optional[Deferred] = None
        self.inprogress: Set[Request] = set()
        self.start_requests: Optional[Iterator[Request]] = iter(start_requests)
        self.close_if_idle: bool = close_if_idle
        self.nextcall: CallLaterOnce = nextcall
        self.scheduler: 'BaseScheduler' = scheduler
        self.heartbeat: LoopingCall = LoopingCall(nextcall.schedule)

class ExecutionEngine:

    def __init__(self, crawler: 'Crawler', spider_closed_callback: Callable) -> None:
        self.crawler: 'Crawler' = crawler
        self.settings: Settings = crawler.settings
        self.signals: SignalManager = crawler.signals
        assert crawler.logformatter
        self.logformatter: LogFormatter = crawler.logformatter
        self.slot: Optional[Slot] = None
        self.spider: Optional[Spider] = None
        self.running: bool = False
        self.paused: bool = False
        self.scheduler_cls: Type['BaseScheduler'] = self._get_scheduler_class(crawler.settings)
        downloader_cls: Type[Downloader] = load_object(self.settings['DOWNLOADER'])
        self.downloader: Downloader = downloader_cls(crawler)
        self.scraper = Scraper(crawler)
        self._spider_closed_callback: Callable = spider_closed_callback
        self.start_time: Optional[float] = None

    def stop(self) -> Deferred:
        """Gracefully stop the execution engine"""
        pass

    def close(self) -> Deferred:
        """
        Gracefully close the execution engine.
        If it has already been started, stop it. In all cases, close the spider and the downloader.
        """
        pass

    def crawl(self, request: Request) -> None:
        """Inject the request into the spider <-> downloader pipeline"""
        pass

    def download(self, request: Request) -> Deferred:
        """Return a Deferred which fires with a Response as result, only downloader middlewares are applied"""
        pass

    def _spider_idle(self) -> None:
        """
        Called when a spider gets idle, i.e. when there are no remaining requests to download or schedule.
        It can be called multiple times. If a handler for the spider_idle signal raises a DontCloseSpider
        exception, the spider is not closed until the next loop and this function is guaranteed to be called
        (at least) once again. A handler can raise CloseSpider to provide a custom closing reason.
        """
        pass

    def close_spider(self, spider: Spider, reason: str='cancelled') -> Deferred:
        """Close (cancel) spider and clear all its outstanding requests"""
        pass