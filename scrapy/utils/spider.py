from __future__ import annotations
import inspect
import logging
from types import CoroutineType, ModuleType
from typing import TYPE_CHECKING, Any, AsyncGenerator, Generator, Iterable, Literal, Optional, Type, TypeVar, Union, overload
from twisted.internet.defer import Deferred
from scrapy import Request
from scrapy.spiders import Spider
from scrapy.utils.defer import deferred_from_coro
from scrapy.utils.misc import arg_to_iter
if TYPE_CHECKING:
    from scrapy.spiderloader import SpiderLoader
logger = logging.getLogger(__name__)
_T = TypeVar('_T')

def iter_spider_classes(module: ModuleType) -> Generator[Type[Spider], Any, None]:
    """Return an iterator over all spider classes defined in the given module
    that can be instantiated (i.e. which have name)
    """
    pass

def spidercls_for_request(spider_loader: SpiderLoader, request: Request, default_spidercls: Optional[Type[Spider]]=None, log_none: bool=False, log_multiple: bool=False) -> Optional[Type[Spider]]:
    """Return a spider class that handles the given Request.

    This will look for the spiders that can handle the given request (using
    the spider loader) and return a Spider class if (and only if) there is
    only one Spider able to handle the Request.

    If multiple spiders (or no spider) are found, it will return the
    default_spidercls passed. It can optionally log if multiple or no spiders
    are found.
    """
    pass

class DefaultSpider(Spider):
    name = 'default'