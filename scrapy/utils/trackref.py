"""This module provides some functions and classes to record and report
references to live object instances.

If you want live objects for a particular class to be tracked, you only have to
subclass from object_ref (instead of object).

About performance: This library has a minimal performance impact when enabled,
and no performance penalty at all when disabled (as object_ref becomes just an
alias to object in that case).
"""
from collections import defaultdict
from operator import itemgetter
from time import time
from typing import TYPE_CHECKING, Any, DefaultDict, Iterable
from weakref import WeakKeyDictionary
if TYPE_CHECKING:
    from typing_extensions import Self
NoneType = type(None)
live_refs: DefaultDict[type, WeakKeyDictionary] = defaultdict(WeakKeyDictionary)

class object_ref:
    """Inherit from this class to a keep a record of live instances"""
    __slots__ = ()

    def __new__(cls, *args: Any, **kwargs: Any) -> 'Self':
        obj = object.__new__(cls)
        live_refs[cls][obj] = time()
        return obj

def format_live_refs(ignore: Any=NoneType) -> str:
    """Return a tabular representation of tracked objects"""
    pass

def print_live_refs(*a: Any, **kw: Any) -> None:
    """Print tracked objects"""
    pass

def get_oldest(class_name: str) -> Any:
    """Get the oldest object for a specific class name"""
    pass

def iter_all(class_name: str) -> Iterable[Any]:
    """Iterate over all objects of the same class by its class name"""
    pass