"""Helper functions which don't fit anywhere else"""
import ast
import hashlib
import inspect
import os
import re
import warnings
from collections import deque
from contextlib import contextmanager
from functools import partial
from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType
from typing import IO, TYPE_CHECKING, Any, Callable, Deque, Generator, Iterable, List, Optional, Pattern, Union, cast
from w3lib.html import replace_entities
from scrapy.item import Item
from scrapy.utils.datatypes import LocalWeakReferencedCache
from scrapy.utils.deprecate import ScrapyDeprecationWarning
from scrapy.utils.python import flatten, to_unicode
if TYPE_CHECKING:
    from scrapy import Spider
_ITERABLE_SINGLE_VALUES = (dict, Item, str, bytes)

def arg_to_iter(arg: Any) -> Iterable[Any]:
    """Convert an argument to an iterable. The argument can be a None, single
    value, or an iterable.

    Exception: if arg is a dict, [arg] will be returned
    """
    pass

def load_object(path: Union[str, Callable]) -> Any:
    """Load an object given its absolute object path, and return it.

    The object can be the import path of a class, function, variable or an
    instance, e.g. 'scrapy.downloadermiddlewares.redirect.RedirectMiddleware'.

    If ``path`` is not a string, but is a callable object, such as a class or
    a function, then return it as is.
    """
    pass

def walk_modules(path: str) -> List[ModuleType]:
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.

    For example: walk_modules('scrapy.utils')
    """
    pass

def extract_regex(regex: Union[str, Pattern], text: str, encoding: str='utf-8') -> List[str]:
    """Extract a list of unicode strings from the given text/encoding using the following policies:

    * if the regex contains a named group called "extract" that will be returned
    * if the regex contains multiple numbered groups, all those will be returned (flattened)
    * if the regex doesn't contain any group the entire regex matching is returned
    """
    pass

def md5sum(file: IO) -> str:
    """Calculate the md5 checksum of a file-like object without reading its
    whole content in memory.

    >>> from io import BytesIO
    >>> md5sum(BytesIO(b'file content to hash'))
    '784406af91dd5a54fbb9c84c2236595a'
    """
    pass

def rel_has_nofollow(rel: Optional[str]) -> bool:
    """Return True if link rel attribute has nofollow type"""
    pass

def create_instance(objcls, settings, crawler, *args, **kwargs):
    """Construct a class instance using its ``from_crawler`` or
    ``from_settings`` constructors, if available.

    At least one of ``settings`` and ``crawler`` needs to be different from
    ``None``. If ``settings `` is ``None``, ``crawler.settings`` will be used.
    If ``crawler`` is ``None``, only the ``from_settings`` constructor will be
    tried.

    ``*args`` and ``**kwargs`` are forwarded to the constructors.

    Raises ``ValueError`` if both ``settings`` and ``crawler`` are ``None``.

    .. versionchanged:: 2.2
       Raises ``TypeError`` if the resulting instance is ``None`` (e.g. if an
       extension has not been implemented correctly).
    """
    pass

@contextmanager
def set_environ(**kwargs: str) -> Generator[None, Any, None]:
    """Temporarily set environment variables inside the context manager and
    fully restore previous environment afterwards
    """
    pass

def walk_callable(node: ast.AST) -> Generator[ast.AST, Any, None]:
    """Similar to ``ast.walk``, but walks only function body and skips nested
    functions defined within the node.
    """
    pass
_generator_callbacks_cache = LocalWeakReferencedCache(limit=128)

def is_generator_with_return_value(callable: Callable) -> bool:
    """
    Returns True if a callable is a generator function which includes a
    'return' statement with a value different than None, False otherwise
    """
    pass

def warn_on_generator_with_return_value(spider: 'Spider', callable: Callable) -> None:
    """
    Logs a warning if a callable is a generator function and includes
    a 'return' statement with a value different than None
    """
    pass