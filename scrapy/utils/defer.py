"""
Helper functions for dealing with Twisted deferreds
"""
import asyncio
import inspect
from asyncio import Future
from functools import wraps
from types import CoroutineType
from typing import Any, AsyncGenerator, AsyncIterable, AsyncIterator, Awaitable, Callable, Coroutine, Dict, Generator, Iterable, Iterator, List, Optional, Tuple, TypeVar, Union, cast, overload
from twisted.internet import defer
from twisted.internet.defer import Deferred, DeferredList, ensureDeferred
from twisted.internet.task import Cooperator
from twisted.python import failure
from twisted.python.failure import Failure
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.reactor import _get_asyncio_event_loop, is_asyncio_reactor_installed

def defer_fail(_failure: Failure) -> Deferred:
    """Same as twisted.internet.defer.fail but delay calling errback until
    next reactor loop

    It delays by 100ms so reactor has a chance to go through readers and writers
    before attending pending delayed calls, so do not set delay to zero.
    """
    pass

def defer_succeed(result: Any) -> Deferred:
    """Same as twisted.internet.defer.succeed but delay calling callback until
    next reactor loop

    It delays by 100ms so reactor has a chance to go through readers and writers
    before attending pending delayed calls, so do not set delay to zero.
    """
    pass

def mustbe_deferred(f: Callable, *args: Any, **kw: Any) -> Deferred:
    """Same as twisted.internet.defer.maybeDeferred, but delay calling
    callback/errback to next reactor loop
    """
    pass

def parallel(iterable: Iterable, count: int, callable: Callable, *args: Any, **named: Any) -> Deferred:
    """Execute a callable over the objects in the given iterable, in parallel,
    using no more than ``count`` concurrent calls.

    Taken from: https://jcalderone.livejournal.com/24285.html
    """
    pass

class _AsyncCooperatorAdapter(Iterator):
    """A class that wraps an async iterable into a normal iterator suitable
    for using in Cooperator.coiterate(). As it's only needed for parallel_async(),
    it calls the callable directly in the callback, instead of providing a more
    generic interface.

    On the outside, this class behaves as an iterator that yields Deferreds.
    Each Deferred is fired with the result of the callable which was called on
    the next result from aiterator. It raises StopIteration when aiterator is
    exhausted, as expected.

    Cooperator calls __next__() multiple times and waits on the Deferreds
    returned from it. As async generators (since Python 3.8) don't support
    awaiting on __anext__() several times in parallel, we need to serialize
    this. It's done by storing the Deferreds returned from __next__() and
    firing the oldest one when a result from __anext__() is available.

    The workflow:
    1. When __next__() is called for the first time, it creates a Deferred, stores it
    in self.waiting_deferreds and returns it. It also makes a Deferred that will wait
    for self.aiterator.__anext__() and puts it into self.anext_deferred.
    2. If __next__() is called again before self.anext_deferred fires, more Deferreds
    are added to self.waiting_deferreds.
    3. When self.anext_deferred fires, it either calls _callback() or _errback(). Both
    clear self.anext_deferred.
    3.1. _callback() calls the callable passing the result value that it takes, pops a
    Deferred from self.waiting_deferreds, and if the callable result was a Deferred, it
    chains those Deferreds so that the waiting Deferred will fire when the result
    Deferred does, otherwise it fires it directly. This causes one awaiting task to
    receive a result. If self.waiting_deferreds is still not empty, new __anext__() is
    called and self.anext_deferred is populated.
    3.2. _errback() checks the exception class. If it's StopAsyncIteration it means
    self.aiterator is exhausted and so it sets self.finished and fires all
    self.waiting_deferreds. Other exceptions are propagated.
    4. If __next__() is called after __anext__() was handled, then if self.finished is
    True, it raises StopIteration, otherwise it acts like in step 2, but if
    self.anext_deferred is now empty is also populates it with a new __anext__().

    Note that CooperativeTask ignores the value returned from the Deferred that it waits
    for, so we fire them with None when needed.

    It may be possible to write an async iterator-aware replacement for
    Cooperator/CooperativeTask and use it instead of this adapter to achieve the same
    goal.
    """

    def __init__(self, aiterable: AsyncIterable, callable: Callable, *callable_args: Any, **callable_kwargs: Any):
        self.aiterator: AsyncIterator = aiterable.__aiter__()
        self.callable: Callable = callable
        self.callable_args: Tuple[Any, ...] = callable_args
        self.callable_kwargs: Dict[str, Any] = callable_kwargs
        self.finished: bool = False
        self.waiting_deferreds: List[Deferred] = []
        self.anext_deferred: Optional[Deferred] = None

    def __next__(self) -> Deferred:
        if self.finished:
            raise StopIteration
        d: Deferred = Deferred()
        self.waiting_deferreds.append(d)
        if not self.anext_deferred:
            self._call_anext()
        return d

def parallel_async(async_iterable: AsyncIterable, count: int, callable: Callable, *args: Any, **named: Any) -> Deferred:
    """Like parallel but for async iterators"""
    pass

def process_chain(callbacks: Iterable[Callable], input: Any, *a: Any, **kw: Any) -> Deferred:
    """Return a Deferred built by chaining the given callbacks"""
    pass

def process_chain_both(callbacks: Iterable[Callable], errbacks: Iterable[Callable], input: Any, *a: Any, **kw: Any) -> Deferred:
    """Return a Deferred built by chaining the given callbacks and errbacks"""
    pass

def process_parallel(callbacks: Iterable[Callable], input: Any, *a: Any, **kw: Any) -> Deferred:
    """Return a Deferred with the output of all successful calls to the given
    callbacks
    """
    pass

def iter_errback(iterable: Iterable, errback: Callable, *a: Any, **kw: Any) -> Generator:
    """Wraps an iterable calling an errback if an error is caught while
    iterating it.
    """
    pass

async def aiter_errback(aiterable: AsyncIterable, errback: Callable, *a: Any, **kw: Any) -> AsyncGenerator:
    """Wraps an async iterable calling an errback if an error is caught while
    iterating it. Similar to scrapy.utils.defer.iter_errback()
    """
    pass
_CT = TypeVar('_CT', bound=Union[Awaitable, CoroutineType, Future])
_T = TypeVar('_T')

def deferred_from_coro(o: _T) -> Union[Deferred, _T]:
    """Converts a coroutine into a Deferred, or returns the object as is if it isn't a coroutine"""
    pass

def deferred_f_from_coro_f(coro_f: Callable[..., Coroutine]) -> Callable:
    """Converts a coroutine function into a function that returns a Deferred.

    The coroutine function will be called at the time when the wrapper is called. Wrapper args will be passed to it.
    This is useful for callback chains, as callback functions are called with the previous callback result.
    """
    pass

def maybeDeferred_coro(f: Callable, *args: Any, **kw: Any) -> Deferred:
    """Copy of defer.maybeDeferred that also converts coroutines to Deferreds."""
    pass

def deferred_to_future(d: Deferred) -> Future:
    """
    .. versionadded:: 2.6.0

    Return an :class:`asyncio.Future` object that wraps *d*.

    When :ref:`using the asyncio reactor <install-asyncio>`, you cannot await
    on :class:`~twisted.internet.defer.Deferred` objects from :ref:`Scrapy
    callables defined as coroutines <coroutine-support>`, you can only await on
    ``Future`` objects. Wrapping ``Deferred`` objects into ``Future`` objects
    allows you to wait on them::

        class MySpider(Spider):
            ...
            async def parse(self, response):
                additional_request = scrapy.Request('https://example.org/price')
                deferred = self.crawler.engine.download(additional_request)
                additional_response = await deferred_to_future(deferred)
    """
    pass

def maybe_deferred_to_future(d: Deferred) -> Union[Deferred, Future]:
    """
    .. versionadded:: 2.6.0

    Return *d* as an object that can be awaited from a :ref:`Scrapy callable
    defined as a coroutine <coroutine-support>`.

    What you can await in Scrapy callables defined as coroutines depends on the
    value of :setting:`TWISTED_REACTOR`:

    -   When not using the asyncio reactor, you can only await on
        :class:`~twisted.internet.defer.Deferred` objects.

    -   When :ref:`using the asyncio reactor <install-asyncio>`, you can only
        await on :class:`asyncio.Future` objects.

    If you want to write code that uses ``Deferred`` objects but works with any
    reactor, use this function on all ``Deferred`` objects::

        class MySpider(Spider):
            ...
            async def parse(self, response):
                additional_request = scrapy.Request('https://example.org/price')
                deferred = self.crawler.engine.download(additional_request)
                additional_response = await maybe_deferred_to_future(deferred)
    """
    pass