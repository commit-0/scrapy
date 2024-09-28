"""
This module implements a class which returns the appropriate Response class
based on different criteria.
"""
from io import StringIO
from mimetypes import MimeTypes
from pkgutil import get_data
from typing import Dict, Mapping, Optional, Type, Union
from scrapy.http import Response
from scrapy.utils.misc import load_object
from scrapy.utils.python import binary_is_text, to_bytes, to_unicode

class ResponseTypes:
    CLASSES = {'text/html': 'scrapy.http.HtmlResponse', 'application/atom+xml': 'scrapy.http.XmlResponse', 'application/rdf+xml': 'scrapy.http.XmlResponse', 'application/rss+xml': 'scrapy.http.XmlResponse', 'application/xhtml+xml': 'scrapy.http.HtmlResponse', 'application/vnd.wap.xhtml+xml': 'scrapy.http.HtmlResponse', 'application/xml': 'scrapy.http.XmlResponse', 'application/json': 'scrapy.http.TextResponse', 'application/x-json': 'scrapy.http.TextResponse', 'application/json-amazonui-streaming': 'scrapy.http.TextResponse', 'application/javascript': 'scrapy.http.TextResponse', 'application/x-javascript': 'scrapy.http.TextResponse', 'text/xml': 'scrapy.http.XmlResponse', 'text/*': 'scrapy.http.TextResponse'}

    def __init__(self) -> None:
        self.classes: Dict[str, Type[Response]] = {}
        self.mimetypes: MimeTypes = MimeTypes()
        mimedata = get_data('scrapy', 'mime.types')
        if not mimedata:
            raise ValueError('The mime.types file is not found in the Scrapy installation')
        self.mimetypes.readfp(StringIO(mimedata.decode('utf8')))
        for mimetype, cls in self.CLASSES.items():
            self.classes[mimetype] = load_object(cls)

    def from_mimetype(self, mimetype: str) -> Type[Response]:
        """Return the most appropriate Response class for the given mimetype"""
        pass

    def from_content_type(self, content_type: Union[str, bytes], content_encoding: Optional[bytes]=None) -> Type[Response]:
        """Return the most appropriate Response class from an HTTP Content-Type
        header"""
        pass

    def from_headers(self, headers: Mapping[bytes, bytes]) -> Type[Response]:
        """Return the most appropriate Response class by looking at the HTTP
        headers"""
        pass

    def from_filename(self, filename: str) -> Type[Response]:
        """Return the most appropriate Response class from a file name"""
        pass

    def from_body(self, body: bytes) -> Type[Response]:
        """Try to guess the appropriate response based on the body content.
        This method is a bit magic and could be improved in the future, but
        it's not meant to be used except for special cases where response types
        cannot be guess using more straightforward methods."""
        pass

    def from_args(self, headers: Optional[Mapping[bytes, bytes]]=None, url: Optional[str]=None, filename: Optional[str]=None, body: Optional[bytes]=None) -> Type[Response]:
        """Guess the most appropriate Response class based on
        the given arguments."""
        pass
responsetypes = ResponseTypes()