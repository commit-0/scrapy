import warnings
from functools import wraps
from typing import Any, Callable
from twisted.internet import defer, threads
from twisted.internet.defer import Deferred
from scrapy.exceptions import ScrapyDeprecationWarning

def deprecated(use_instead: Any=None) -> Callable:
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    pass

def defers(func: Callable) -> Callable[..., Deferred]:
    """Decorator to make sure a function always returns a deferred"""
    pass

def inthread(func: Callable) -> Callable[..., Deferred]:
    """Decorator to call a function in a thread and return a deferred with the
    result
    """
    pass