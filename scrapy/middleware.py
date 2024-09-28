from __future__ import annotations
import logging
import pprint
from collections import defaultdict, deque
from typing import TYPE_CHECKING, Any, Callable, Deque, Dict, Iterable, List, Optional, Tuple, Union, cast
from twisted.internet.defer import Deferred
from scrapy import Spider
from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings
from scrapy.utils.defer import process_chain, process_parallel
from scrapy.utils.misc import create_instance, load_object
if TYPE_CHECKING:
    from typing_extensions import Self
    from scrapy.crawler import Crawler
logger = logging.getLogger(__name__)

class MiddlewareManager:
    """Base class for implementing middleware managers"""
    component_name = 'foo middleware'

    def __init__(self, *middlewares: Any) -> None:
        self.middlewares = middlewares
        self.methods: Dict[str, Deque[Union[None, Callable, Tuple[Callable, Callable]]]] = defaultdict(deque)
        for mw in middlewares:
            self._add_middleware(mw)