from __future__ import annotations
import logging
import pprint
import signal
import warnings
from typing import TYPE_CHECKING, Any, Dict, Generator, Optional, Set, Type, Union, cast
from twisted.internet.defer import Deferred, DeferredList, inlineCallbacks, maybeDeferred
from zope.interface.exceptions import DoesNotImplement
try:
    from zope.interface.exceptions import MultipleInvalid
except ImportError:
    MultipleInvalid = None
from zope.interface.verify import verifyClass
from scrapy import Spider, signals
from scrapy.addons import AddonManager
from scrapy.core.engine import ExecutionEngine
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.extension import ExtensionManager
from scrapy.interfaces import ISpiderLoader
from scrapy.logformatter import LogFormatter
from scrapy.settings import BaseSettings, Settings, overridden_settings
from scrapy.signalmanager import SignalManager
from scrapy.statscollectors import StatsCollector
from scrapy.utils.log import LogCounterHandler, configure_logging, get_scrapy_root_handler, install_scrapy_root_handler, log_reactor_info, log_scrapy_info
from scrapy.utils.misc import create_instance, load_object
from scrapy.utils.ossignal import install_shutdown_handlers, signal_names
from scrapy.utils.reactor import install_reactor, is_asyncio_reactor_installed, verify_installed_asyncio_event_loop, verify_installed_reactor
if TYPE_CHECKING:
    from scrapy.utils.request import RequestFingerprinter
logger = logging.getLogger(__name__)

class Crawler:

    def __init__(self, spidercls: Type[Spider], settings: Union[None, Dict[str, Any], Settings]=None, init_reactor: bool=False):
        if isinstance(spidercls, Spider):
            raise ValueError('The spidercls argument must be a class, not an object')
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)
        self.spidercls: Type[Spider] = spidercls
        self.settings: Settings = settings.copy()
        self.spidercls.update_settings(self.settings)
        self._update_root_log_handler()
        self.addons: AddonManager = AddonManager(self)
        self.signals: SignalManager = SignalManager(self)
        self._init_reactor: bool = init_reactor
        self.crawling: bool = False
        self._started: bool = False
        self.extensions: Optional[ExtensionManager] = None
        self.stats: Optional[StatsCollector] = None
        self.logformatter: Optional[LogFormatter] = None
        self.request_fingerprinter: Optional[RequestFingerprinter] = None
        self.spider: Optional[Spider] = None
        self.engine: Optional[ExecutionEngine] = None

    @inlineCallbacks
    def stop(self) -> Generator[Deferred, Any, None]:
        """Starts a graceful stop of the crawler and returns a deferred that is
        fired when the crawler is stopped."""
        pass

class CrawlerRunner:
    """
    This is a convenient helper class that keeps track of, manages and runs
    crawlers inside an already setup :mod:`~twisted.internet.reactor`.

    The CrawlerRunner object must be instantiated with a
    :class:`~scrapy.settings.Settings` object.

    This class shouldn't be needed (since Scrapy is responsible of using it
    accordingly) unless writing scripts that manually handle the crawling
    process. See :ref:`run-from-script` for an example.
    """
    crawlers = property(lambda self: self._crawlers, doc='Set of :class:`crawlers <scrapy.crawler.Crawler>` started by :meth:`crawl` and managed by this class.')

    @staticmethod
    def _get_spider_loader(settings: BaseSettings):
        """Get SpiderLoader instance from settings"""
        pass

    def __init__(self, settings: Union[Dict[str, Any], Settings, None]=None):
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)
        self.settings = settings
        self.spider_loader = self._get_spider_loader(settings)
        self._crawlers: Set[Crawler] = set()
        self._active: Set[Deferred] = set()
        self.bootstrap_failed = False

    def crawl(self, crawler_or_spidercls: Union[Type[Spider], str, Crawler], *args: Any, **kwargs: Any) -> Deferred:
        """
        Run a crawler with the provided arguments.

        It will call the given Crawler's :meth:`~Crawler.crawl` method, while
        keeping track of it so it can be stopped later.

        If ``crawler_or_spidercls`` isn't a :class:`~scrapy.crawler.Crawler`
        instance, this method will try to create one using this parameter as
        the spider class given to it.

        Returns a deferred that is fired when the crawling is finished.

        :param crawler_or_spidercls: already created crawler, or a spider class
            or spider's name inside the project to create it
        :type crawler_or_spidercls: :class:`~scrapy.crawler.Crawler` instance,
            :class:`~scrapy.spiders.Spider` subclass or string

        :param args: arguments to initialize the spider

        :param kwargs: keyword arguments to initialize the spider
        """
        pass

    def create_crawler(self, crawler_or_spidercls: Union[Type[Spider], str, Crawler]) -> Crawler:
        """
        Return a :class:`~scrapy.crawler.Crawler` object.

        * If ``crawler_or_spidercls`` is a Crawler, it is returned as-is.
        * If ``crawler_or_spidercls`` is a Spider subclass, a new Crawler
          is constructed for it.
        * If ``crawler_or_spidercls`` is a string, this function finds
          a spider with this name in a Scrapy project (using spider loader),
          then creates a Crawler instance for it.
        """
        pass

    def stop(self) -> Deferred:
        """
        Stops simultaneously all the crawling jobs taking place.

        Returns a deferred that is fired when they all have ended.
        """
        pass

    @inlineCallbacks
    def join(self) -> Generator[Deferred, Any, None]:
        """
        join()

        Returns a deferred that is fired when all managed :attr:`crawlers` have
        completed their executions.
        """
        pass

class CrawlerProcess(CrawlerRunner):
    """
    A class to run multiple scrapy crawlers in a process simultaneously.

    This class extends :class:`~scrapy.crawler.CrawlerRunner` by adding support
    for starting a :mod:`~twisted.internet.reactor` and handling shutdown
    signals, like the keyboard interrupt command Ctrl-C. It also configures
    top-level logging.

    This utility should be a better fit than
    :class:`~scrapy.crawler.CrawlerRunner` if you aren't running another
    :mod:`~twisted.internet.reactor` within your application.

    The CrawlerProcess object must be instantiated with a
    :class:`~scrapy.settings.Settings` object.

    :param install_root_handler: whether to install root logging handler
        (default: True)

    This class shouldn't be needed (since Scrapy is responsible of using it
    accordingly) unless writing scripts that manually handle the crawling
    process. See :ref:`run-from-script` for an example.
    """

    def __init__(self, settings: Union[Dict[str, Any], Settings, None]=None, install_root_handler: bool=True):
        super().__init__(settings)
        configure_logging(self.settings, install_root_handler)
        log_scrapy_info(self.settings)
        self._initialized_reactor = False

    def start(self, stop_after_crawl: bool=True, install_signal_handlers: bool=True) -> None:
        """
        This method starts a :mod:`~twisted.internet.reactor`, adjusts its pool
        size to :setting:`REACTOR_THREADPOOL_MAXSIZE`, and installs a DNS cache
        based on :setting:`DNSCACHE_ENABLED` and :setting:`DNSCACHE_SIZE`.

        If ``stop_after_crawl`` is True, the reactor will be stopped after all
        crawlers have finished, using :meth:`join`.

        :param bool stop_after_crawl: stop or not the reactor when all
            crawlers have finished

        :param bool install_signal_handlers: whether to install the OS signal
            handlers from Twisted and Scrapy (default: True)
        """
        pass