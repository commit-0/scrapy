"""
This module provides some useful functions for working with
scrapy.http.Request objects
"""
import hashlib
import json
import warnings
from typing import TYPE_CHECKING, Any, Dict, Generator, Iterable, List, Optional, Protocol, Tuple, Type, Union
from urllib.parse import urlunparse
from weakref import WeakKeyDictionary
from w3lib.http import basic_auth_header
from w3lib.url import canonicalize_url
from scrapy import Request, Spider
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.misc import load_object
from scrapy.utils.python import to_bytes, to_unicode
if TYPE_CHECKING:
    from scrapy.crawler import Crawler
_deprecated_fingerprint_cache: 'WeakKeyDictionary[Request, Dict[Tuple[Optional[Tuple[bytes, ...]], bool], str]]'
_deprecated_fingerprint_cache = WeakKeyDictionary()

def request_fingerprint(request: Request, include_headers: Optional[Iterable[Union[bytes, str]]]=None, keep_fragments: bool=False) -> str:
    """
    Return the request fingerprint as an hexadecimal string.

    The request fingerprint is a hash that uniquely identifies the resource the
    request points to. For example, take the following two urls:

    http://www.example.com/query?id=111&cat=222
    http://www.example.com/query?cat=222&id=111

    Even though those are two different URLs both point to the same resource
    and are equivalent (i.e. they should return the same response).

    Another example are cookies used to store session ids. Suppose the
    following page is only accessible to authenticated users:

    http://www.example.com/members/offers.html

    Lots of sites use a cookie to store the session id, which adds a random
    component to the HTTP Request and thus should be ignored when calculating
    the fingerprint.

    For this reason, request headers are ignored by default when calculating
    the fingerprint. If you want to include specific headers use the
    include_headers argument, which is a list of Request headers to include.

    Also, servers usually ignore fragments in urls when handling requests,
    so they are also ignored by default when calculating the fingerprint.
    If you want to include them, set the keep_fragments argument to True
    (for instance when handling requests with a headless browser).
    """
    pass
_fingerprint_cache: 'WeakKeyDictionary[Request, Dict[Tuple[Optional[Tuple[bytes, ...]], bool], bytes]]'
_fingerprint_cache = WeakKeyDictionary()

def fingerprint(request: Request, *, include_headers: Optional[Iterable[Union[bytes, str]]]=None, keep_fragments: bool=False) -> bytes:
    """
    Return the request fingerprint.

    The request fingerprint is a hash that uniquely identifies the resource the
    request points to. For example, take the following two urls:

    http://www.example.com/query?id=111&cat=222
    http://www.example.com/query?cat=222&id=111

    Even though those are two different URLs both point to the same resource
    and are equivalent (i.e. they should return the same response).

    Another example are cookies used to store session ids. Suppose the
    following page is only accessible to authenticated users:

    http://www.example.com/members/offers.html

    Lots of sites use a cookie to store the session id, which adds a random
    component to the HTTP Request and thus should be ignored when calculating
    the fingerprint.

    For this reason, request headers are ignored by default when calculating
    the fingerprint. If you want to include specific headers use the
    include_headers argument, which is a list of Request headers to include.

    Also, servers usually ignore fragments in urls when handling requests,
    so they are also ignored by default when calculating the fingerprint.
    If you want to include them, set the keep_fragments argument to True
    (for instance when handling requests with a headless browser).
    """
    pass

class RequestFingerprinterProtocol(Protocol):
    pass

class RequestFingerprinter:
    """Default fingerprinter.

    It takes into account a canonical version
    (:func:`w3lib.url.canonicalize_url`) of :attr:`request.url
    <scrapy.http.Request.url>` and the values of :attr:`request.method
    <scrapy.http.Request.method>` and :attr:`request.body
    <scrapy.http.Request.body>`. It then generates an `SHA1
    <https://en.wikipedia.org/wiki/SHA-1>`_ hash.

    .. seealso:: :setting:`REQUEST_FINGERPRINTER_IMPLEMENTATION`.
    """

    def __init__(self, crawler: Optional['Crawler']=None):
        if crawler:
            implementation = crawler.settings.get('REQUEST_FINGERPRINTER_IMPLEMENTATION')
        else:
            implementation = '2.6'
        if implementation == '2.6':
            message = "'2.6' is a deprecated value for the 'REQUEST_FINGERPRINTER_IMPLEMENTATION' setting.\n\nIt is also the default value. In other words, it is normal to get this warning if you have not defined a value for the 'REQUEST_FINGERPRINTER_IMPLEMENTATION' setting. This is so for backward compatibility reasons, but it will change in a future version of Scrapy.\n\nSee the documentation of the 'REQUEST_FINGERPRINTER_IMPLEMENTATION' setting for information on how to handle this deprecation."
            warnings.warn(message, category=ScrapyDeprecationWarning, stacklevel=2)
            self._fingerprint = _request_fingerprint_as_bytes
        elif implementation == '2.7':
            self._fingerprint = fingerprint
        else:
            raise ValueError(f"Got an invalid value on setting 'REQUEST_FINGERPRINTER_IMPLEMENTATION': {implementation!r}. Valid values are '2.6' (deprecated) and '2.7'.")

def request_authenticate(request: Request, username: str, password: str) -> None:
    """Authenticate the given request (in place) using the HTTP basic access
    authentication mechanism (RFC 2617) and the given username and password
    """
    pass

def request_httprepr(request: Request) -> bytes:
    """Return the raw HTTP representation (as bytes) of the given request.
    This is provided only for reference since it's not the actual stream of
    bytes that will be send when performing the request (that's controlled
    by Twisted).
    """
    pass

def referer_str(request: Request) -> Optional[str]:
    """Return Referer HTTP header suitable for logging."""
    pass

def request_from_dict(d: dict, *, spider: Optional[Spider]=None) -> Request:
    """Create a :class:`~scrapy.Request` object from a dict.

    If a spider is given, it will try to resolve the callbacks looking at the
    spider for methods with the same name.
    """
    pass

def _get_method(obj: Any, name: Any) -> Any:
    """Helper function for request_from_dict"""
    pass

def request_to_curl(request: Request) -> str:
    """
    Converts a :class:`~scrapy.Request` object to a curl command.

    :param :class:`~scrapy.Request`: Request object to be converted
    :return: string containing the curl command
    """
    pass