"""
This module contains essential stuff that should've come with Python itself ;)
"""
import collections.abc
import gc
import inspect
import re
import sys
import weakref
from functools import partial, wraps
from itertools import chain
from typing import Any, AsyncGenerator, AsyncIterable, AsyncIterator, Callable, Dict, Generator, Iterable, Iterator, List, Mapping, Optional, Pattern, Tuple, Union, overload
from scrapy.utils.asyncgen import as_async_generator

def flatten(x: Iterable) -> list:
    """flatten(sequence) -> list

    Returns a single, flat list which contains all elements retrieved
    from the sequence and all recursively contained sub-sequences
    (iterables).

    Examples:
    >>> [1, 2, [3,4], (5,6)]
    [1, 2, [3, 4], (5, 6)]
    >>> flatten([[[1,2,3], (42,None)], [4,5], [6], 7, (8,9,10)])
    [1, 2, 3, 42, None, 4, 5, 6, 7, 8, 9, 10]
    >>> flatten(["foo", "bar"])
    ['foo', 'bar']
    >>> flatten(["foo", ["baz", 42], "bar"])
    ['foo', 'baz', 42, 'bar']
    """
    pass

def iflatten(x: Iterable) -> Iterable:
    """iflatten(sequence) -> iterator

    Similar to ``.flatten()``, but returns iterator instead"""
    pass

def is_listlike(x: Any) -> bool:
    """
    >>> is_listlike("foo")
    False
    >>> is_listlike(5)
    False
    >>> is_listlike(b"foo")
    False
    >>> is_listlike([b"foo"])
    True
    >>> is_listlike((b"foo",))
    True
    >>> is_listlike({})
    True
    >>> is_listlike(set())
    True
    >>> is_listlike((x for x in range(3)))
    True
    >>> is_listlike(range(5))
    True
    """
    pass

def unique(list_: Iterable, key: Callable[[Any], Any]=lambda x: x) -> list:
    """efficient function to uniquify a list preserving item order"""
    pass

def to_unicode(text: Union[str, bytes], encoding: Optional[str]=None, errors: str='strict') -> str:
    """Return the unicode representation of a bytes object ``text``. If
    ``text`` is already an unicode object, return it as-is."""
    pass

def to_bytes(text: Union[str, bytes], encoding: Optional[str]=None, errors: str='strict') -> bytes:
    """Return the binary representation of ``text``. If ``text``
    is already a bytes object, return it as-is."""
    pass

def re_rsearch(pattern: Union[str, Pattern], text: str, chunk_size: int=1024) -> Optional[Tuple[int, int]]:
    """
    This function does a reverse search in a text using a regular expression
    given in the attribute 'pattern'.
    Since the re module does not provide this functionality, we have to find for
    the expression into chunks of text extracted from the end (for the sake of efficiency).
    At first, a chunk of 'chunk_size' kilobytes is extracted from the end, and searched for
    the pattern. If the pattern is not found, another chunk is extracted, and another
    search is performed.
    This process continues until a match is found, or until the whole file is read.
    In case the pattern wasn't found, None is returned, otherwise it returns a tuple containing
    the start position of the match, and the ending (regarding the entire text).
    """
    pass

def memoizemethod_noargs(method: Callable) -> Callable:
    """Decorator to cache the result of a method (without arguments) using a
    weak reference to its object
    """
    pass
_BINARYCHARS = {i for i in range(32) if to_bytes(chr(i)) not in {b'\x00', b'\t', b'\n', b'\r'}}

def binary_is_text(data: bytes) -> bool:
    """Returns ``True`` if the given ``data`` argument (a ``bytes`` object)
    does not contain unprintable control characters.
    """
    pass

def get_func_args(func: Callable, stripself: bool=False) -> List[str]:
    """Return the argument name list of a callable object"""
    pass

def get_spec(func: Callable) -> Tuple[List[str], Dict[str, Any]]:
    """Returns (args, kwargs) tuple for a function
    >>> import re
    >>> get_spec(re.match)
    (['pattern', 'string'], {'flags': 0})

    >>> class Test:
    ...     def __call__(self, val):
    ...         pass
    ...     def method(self, val, flags=0):
    ...         pass

    >>> get_spec(Test)
    (['self', 'val'], {})

    >>> get_spec(Test.method)
    (['self', 'val'], {'flags': 0})

    >>> get_spec(Test().method)
    (['self', 'val'], {'flags': 0})
    """
    pass

def equal_attributes(obj1: Any, obj2: Any, attributes: Optional[List[Union[str, Callable]]]) -> bool:
    """Compare two objects attributes"""
    pass

def without_none_values(iterable: Union[Mapping, Iterable]) -> Union[dict, Iterable]:
    """Return a copy of ``iterable`` with all ``None`` entries removed.

    If ``iterable`` is a mapping, return a dictionary where all pairs that have
    value ``None`` have been removed.
    """
    pass

def global_object_name(obj: Any) -> str:
    """
    Return full name of a global object.

    >>> from scrapy import Request
    >>> global_object_name(Request)
    'scrapy.http.request.Request'
    """
    pass
if hasattr(sys, 'pypy_version_info'):

class MutableChain(Iterable):
    """
    Thin wrapper around itertools.chain, allowing to add iterables "in-place"
    """

    def __init__(self, *args: Iterable):
        self.data = chain.from_iterable(args)

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> Any:
        return next(self.data)

class MutableAsyncChain(AsyncIterable):
    """
    Similar to MutableChain but for async iterables
    """

    def __init__(self, *args: Union[Iterable, AsyncIterable]):
        self.data = _async_chain(*args)

    def __aiter__(self) -> AsyncIterator:
        return self

    async def __anext__(self) -> Any:
        return await self.data.__anext__()