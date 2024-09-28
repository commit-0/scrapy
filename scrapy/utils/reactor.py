import asyncio
import sys
from asyncio import AbstractEventLoop, AbstractEventLoopPolicy
from contextlib import suppress
from typing import Any, Callable, Dict, Optional, Sequence, Type
from warnings import catch_warnings, filterwarnings, warn
from twisted.internet import asyncioreactor, error
from twisted.internet.base import DelayedCall
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.utils.misc import load_object

def listen_tcp(portrange, host, factory):
    """Like reactor.listenTCP but tries different ports in a range."""
    pass

class CallLaterOnce:
    """Schedule a function to be called in the next reactor loop, but only if
    it hasn't been already scheduled since the last time it ran.
    """

    def __init__(self, func: Callable, *a: Any, **kw: Any):
        self._func: Callable = func
        self._a: Sequence[Any] = a
        self._kw: Dict[str, Any] = kw
        self._call: Optional[DelayedCall] = None

    def __call__(self) -> Any:
        self._call = None
        return self._func(*self._a, **self._kw)

def set_asyncio_event_loop_policy() -> None:
    """The policy functions from asyncio often behave unexpectedly,
    so we restrict their use to the absolutely essential case.
    This should only be used to install the reactor.
    """
    pass

def install_reactor(reactor_path: str, event_loop_path: Optional[str]=None) -> None:
    """Installs the :mod:`~twisted.internet.reactor` with the specified
    import path. Also installs the asyncio event loop with the specified import
    path if the asyncio reactor is enabled"""
    pass

def set_asyncio_event_loop(event_loop_path: Optional[str]) -> AbstractEventLoop:
    """Sets and returns the event loop with specified import path."""
    pass

def verify_installed_reactor(reactor_path: str) -> None:
    """Raises :exc:`Exception` if the installed
    :mod:`~twisted.internet.reactor` does not match the specified import
    path."""
    pass