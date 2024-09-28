"""
Spider Middleware manager

See documentation in docs/topics/spider-middleware.rst
"""
import logging
from inspect import isasyncgenfunction, iscoroutine
from itertools import islice
from typing import Any, AsyncGenerator, AsyncIterable, Callable, Generator, Iterable, List, Optional, Tuple, Union, cast
from twisted.internet.defer import Deferred, inlineCallbacks
from twisted.python.failure import Failure
from scrapy import Request, Spider
from scrapy.exceptions import _InvalidOutput
from scrapy.http import Response
from scrapy.middleware import MiddlewareManager
from scrapy.settings import BaseSettings
from scrapy.utils.asyncgen import as_async_generator, collect_asyncgen
from scrapy.utils.conf import build_component_list
from scrapy.utils.defer import deferred_f_from_coro_f, deferred_from_coro, maybe_deferred_to_future, mustbe_deferred
from scrapy.utils.python import MutableAsyncChain, MutableChain
logger = logging.getLogger(__name__)
ScrapeFunc = Callable[[Union[Response, Failure], Request, Spider], Any]

class SpiderMiddlewareManager(MiddlewareManager):
    component_name = 'spider middleware'

    def __init__(self, *middlewares: Any):
        super().__init__(*middlewares)
        self.downgrade_warning_done = False