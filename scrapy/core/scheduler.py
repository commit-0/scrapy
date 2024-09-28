from __future__ import annotations
import json
import logging
from abc import abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar, cast
from twisted.internet.defer import Deferred
from scrapy.crawler import Crawler
from scrapy.dupefilters import BaseDupeFilter
from scrapy.http.request import Request
from scrapy.spiders import Spider
from scrapy.statscollectors import StatsCollector
from scrapy.utils.job import job_dir
from scrapy.utils.misc import create_instance, load_object
if TYPE_CHECKING:
    from typing_extensions import Self
logger = logging.getLogger(__name__)

class BaseSchedulerMeta(type):
    """
    Metaclass to check scheduler classes against the necessary interface
    """

    def __instancecheck__(cls, instance: Any) -> bool:
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass: type) -> bool:
        return hasattr(subclass, 'has_pending_requests') and callable(subclass.has_pending_requests) and hasattr(subclass, 'enqueue_request') and callable(subclass.enqueue_request) and hasattr(subclass, 'next_request') and callable(subclass.next_request)

class BaseScheduler(metaclass=BaseSchedulerMeta):
    """
    The scheduler component is responsible for storing requests received from
    the engine, and feeding them back upon request (also to the engine).

    The original sources of said requests are:

    * Spider: ``start_requests`` method, requests created for URLs in the ``start_urls`` attribute, request callbacks
    * Spider middleware: ``process_spider_output`` and ``process_spider_exception`` methods
    * Downloader middleware: ``process_request``, ``process_response`` and ``process_exception`` methods

    The order in which the scheduler returns its stored requests (via the ``next_request`` method)
    plays a great part in determining the order in which those requests are downloaded.

    The methods defined in this class constitute the minimal interface that the Scrapy engine will interact with.
    """

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        """
        Factory method which receives the current :class:`~scrapy.crawler.Crawler` object as argument.
        """
        pass

    def open(self, spider: Spider) -> Optional[Deferred]:
        """
        Called when the spider is opened by the engine. It receives the spider
        instance as argument and it's useful to execute initialization code.

        :param spider: the spider object for the current crawl
        :type spider: :class:`~scrapy.spiders.Spider`
        """
        pass

    def close(self, reason: str) -> Optional[Deferred]:
        """
        Called when the spider is closed by the engine. It receives the reason why the crawl
        finished as argument and it's useful to execute cleaning code.

        :param reason: a string which describes the reason why the spider was closed
        :type reason: :class:`str`
        """
        pass

    @abstractmethod
    def has_pending_requests(self) -> bool:
        """
        ``True`` if the scheduler has enqueued requests, ``False`` otherwise
        """
        pass

    @abstractmethod
    def enqueue_request(self, request: Request) -> bool:
        """
        Process a request received by the engine.

        Return ``True`` if the request is stored correctly, ``False`` otherwise.

        If ``False``, the engine will fire a ``request_dropped`` signal, and
        will not make further attempts to schedule the request at a later time.
        For reference, the default Scrapy scheduler returns ``False`` when the
        request is rejected by the dupefilter.
        """
        pass

    @abstractmethod
    def next_request(self) -> Optional[Request]:
        """
        Return the next :class:`~scrapy.http.Request` to be processed, or ``None``
        to indicate that there are no requests to be considered ready at the moment.

        Returning ``None`` implies that no request from the scheduler will be sent
        to the downloader in the current reactor cycle. The engine will continue
        calling ``next_request`` until ``has_pending_requests`` is ``False``.
        """
        pass
SchedulerTV = TypeVar('SchedulerTV', bound='Scheduler')

class Scheduler(BaseScheduler):
    """
    Default Scrapy scheduler. This implementation also handles duplication
    filtering via the :setting:`dupefilter <DUPEFILTER_CLASS>`.

    This scheduler stores requests into several priority queues (defined by the
    :setting:`SCHEDULER_PRIORITY_QUEUE` setting). In turn, said priority queues
    are backed by either memory or disk based queues (respectively defined by the
    :setting:`SCHEDULER_MEMORY_QUEUE` and :setting:`SCHEDULER_DISK_QUEUE` settings).

    Request prioritization is almost entirely delegated to the priority queue. The only
    prioritization performed by this scheduler is using the disk-based queue if present
    (i.e. if the :setting:`JOBDIR` setting is defined) and falling back to the memory-based
    queue if a serialization error occurs. If the disk queue is not present, the memory one
    is used directly.

    :param dupefilter: An object responsible for checking and filtering duplicate requests.
                       The value for the :setting:`DUPEFILTER_CLASS` setting is used by default.
    :type dupefilter: :class:`scrapy.dupefilters.BaseDupeFilter` instance or similar:
                      any class that implements the `BaseDupeFilter` interface

    :param jobdir: The path of a directory to be used for persisting the crawl's state.
                   The value for the :setting:`JOBDIR` setting is used by default.
                   See :ref:`topics-jobs`.
    :type jobdir: :class:`str` or ``None``

    :param dqclass: A class to be used as persistent request queue.
                    The value for the :setting:`SCHEDULER_DISK_QUEUE` setting is used by default.
    :type dqclass: class

    :param mqclass: A class to be used as non-persistent request queue.
                    The value for the :setting:`SCHEDULER_MEMORY_QUEUE` setting is used by default.
    :type mqclass: class

    :param logunser: A boolean that indicates whether or not unserializable requests should be logged.
                     The value for the :setting:`SCHEDULER_DEBUG` setting is used by default.
    :type logunser: bool

    :param stats: A stats collector object to record stats about the request scheduling process.
                  The value for the :setting:`STATS_CLASS` setting is used by default.
    :type stats: :class:`scrapy.statscollectors.StatsCollector` instance or similar:
                 any class that implements the `StatsCollector` interface

    :param pqclass: A class to be used as priority queue for requests.
                    The value for the :setting:`SCHEDULER_PRIORITY_QUEUE` setting is used by default.
    :type pqclass: class

    :param crawler: The crawler object corresponding to the current crawl.
    :type crawler: :class:`scrapy.crawler.Crawler`
    """

    def __init__(self, dupefilter: BaseDupeFilter, jobdir: Optional[str]=None, dqclass=None, mqclass=None, logunser: bool=False, stats: Optional[StatsCollector]=None, pqclass=None, crawler: Optional[Crawler]=None):
        self.df: BaseDupeFilter = dupefilter
        self.dqdir: Optional[str] = self._dqdir(jobdir)
        self.pqclass = pqclass
        self.dqclass = dqclass
        self.mqclass = mqclass
        self.logunser: bool = logunser
        self.stats: Optional[StatsCollector] = stats
        self.crawler: Optional[Crawler] = crawler

    @classmethod
    def from_crawler(cls: Type[SchedulerTV], crawler: Crawler) -> SchedulerTV:
        """
        Factory method, initializes the scheduler with arguments taken from the crawl settings
        """
        pass

    def open(self, spider: Spider) -> Optional[Deferred]:
        """
        (1) initialize the memory queue
        (2) initialize the disk queue if the ``jobdir`` attribute is a valid directory
        (3) return the result of the dupefilter's ``open`` method
        """
        pass

    def close(self, reason: str) -> Optional[Deferred]:
        """
        (1) dump pending requests to disk if there is a disk queue
        (2) return the result of the dupefilter's ``close`` method
        """
        pass

    def enqueue_request(self, request: Request) -> bool:
        """
        Unless the received request is filtered out by the Dupefilter, attempt to push
        it into the disk queue, falling back to pushing it into the memory queue.

        Increment the appropriate stats, such as: ``scheduler/enqueued``,
        ``scheduler/enqueued/disk``, ``scheduler/enqueued/memory``.

        Return ``True`` if the request was stored successfully, ``False`` otherwise.
        """
        pass

    def next_request(self) -> Optional[Request]:
        """
        Return a :class:`~scrapy.http.Request` object from the memory queue,
        falling back to the disk queue if the memory queue is empty.
        Return ``None`` if there are no more enqueued requests.

        Increment the appropriate stats, such as: ``scheduler/dequeued``,
        ``scheduler/dequeued/disk``, ``scheduler/dequeued/memory``.
        """
        pass

    def __len__(self) -> int:
        """
        Return the total amount of enqueued requests
        """
        return len(self.dqs) + len(self.mqs) if self.dqs is not None else len(self.mqs)

    def _mq(self):
        """Create a new priority queue instance, with in-memory storage"""
        pass

    def _dq(self):
        """Create a new priority queue instance, with disk storage"""
        pass

    def _dqdir(self, jobdir: Optional[str]) -> Optional[str]:
        """Return a folder name to keep disk queue state at"""
        pass