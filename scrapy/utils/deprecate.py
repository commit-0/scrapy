"""Some helpers for deprecation messages"""
import inspect
import warnings
from typing import Any, Dict, List, Optional, Tuple, Type, overload
from scrapy.exceptions import ScrapyDeprecationWarning

def create_deprecated_class(name: str, new_class: type, clsdict: Optional[Dict[str, Any]]=None, warn_category: Type[Warning]=ScrapyDeprecationWarning, warn_once: bool=True, old_class_path: Optional[str]=None, new_class_path: Optional[str]=None, subclass_warn_message: str='{cls} inherits from deprecated class {old}, please inherit from {new}.', instance_warn_message: str='{cls} is deprecated, instantiate {new} instead.') -> type:
    """
    Return a "deprecated" class that causes its subclasses to issue a warning.
    Subclasses of ``new_class`` are considered subclasses of this class.
    It also warns when the deprecated class is instantiated, but do not when
    its subclasses are instantiated.

    It can be used to rename a base class in a library. For example, if we
    have

        class OldName(SomeClass):
            # ...

    and we want to rename it to NewName, we can do the following::

        class NewName(SomeClass):
            # ...

        OldName = create_deprecated_class('OldName', NewName)

    Then, if user class inherits from OldName, warning is issued. Also, if
    some code uses ``issubclass(sub, OldName)`` or ``isinstance(sub(), OldName)``
    checks they'll still return True if sub is a subclass of NewName instead of
    OldName.
    """
    pass
DEPRECATION_RULES: List[Tuple[str, str]] = []

def update_classpath(path: Any) -> Any:
    """Update a deprecated path from an object with its new location"""
    pass

def method_is_overridden(subclass: type, base_class: type, method_name: str) -> bool:
    """
    Return True if a method named ``method_name`` of a ``base_class``
    is overridden in a ``subclass``.

    >>> class Base:
    ...     def foo(self):
    ...         pass
    >>> class Sub1(Base):
    ...     pass
    >>> class Sub2(Base):
    ...     def foo(self):
    ...         pass
    >>> class Sub3(Sub1):
    ...     def foo(self):
    ...         pass
    >>> class Sub4(Sub2):
    ...     pass
    >>> method_is_overridden(Sub1, Base, 'foo')
    False
    >>> method_is_overridden(Sub2, Base, 'foo')
    True
    >>> method_is_overridden(Sub3, Base, 'foo')
    True
    >>> method_is_overridden(Sub4, Base, 'foo')
    True
    """
    pass