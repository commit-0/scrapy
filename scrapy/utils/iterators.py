import csv
import logging
import re
from io import StringIO
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, Iterable, List, Literal, Optional, Union, cast, overload
from warnings import warn
from lxml import etree
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.http import Response, TextResponse
from scrapy.selector import Selector
from scrapy.utils.python import re_rsearch, to_unicode
if TYPE_CHECKING:
    from lxml._types import SupportsReadClose
logger = logging.getLogger(__name__)

def xmliter(obj: Union[Response, str, bytes], nodename: str) -> Generator[Selector, Any, None]:
    """Return a iterator of Selector's over all nodes of a XML document,
       given the name of the node to iterate. Useful for parsing XML feeds.

    obj can be:
    - a Response object
    - a unicode string
    - a string encoded as utf-8
    """
    pass

class _StreamReader:

    def __init__(self, obj: Union[Response, str, bytes]):
        self._ptr: int = 0
        self._text: Union[str, bytes]
        if isinstance(obj, TextResponse):
            self._text, self.encoding = (obj.body, obj.encoding)
        elif isinstance(obj, Response):
            self._text, self.encoding = (obj.body, 'utf-8')
        else:
            self._text, self.encoding = (obj, 'utf-8')
        self._is_unicode: bool = isinstance(self._text, str)
        self._is_first_read: bool = True

def csviter(obj: Union[Response, str, bytes], delimiter: Optional[str]=None, headers: Optional[List[str]]=None, encoding: Optional[str]=None, quotechar: Optional[str]=None) -> Generator[Dict[str, str], Any, None]:
    """Returns an iterator of dictionaries from the given csv object

    obj can be:
    - a Response object
    - a unicode string
    - a string encoded as utf-8

    delimiter is the character used to separate fields on the given obj.

    headers is an iterable that when provided offers the keys
    for the returned dictionaries, if not the first row is used.

    quotechar is the character used to enclosure fields on the given obj.
    """
    pass