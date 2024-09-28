"""
This module implements the FormRequest class which is a more convenient class
(than Request) to generate Requests based on form data.

See documentation in docs/topics/request-response.rst
"""
from typing import Iterable, List, Optional, Tuple, Type, TypeVar, Union, cast
from urllib.parse import urlencode, urljoin, urlsplit, urlunsplit
from lxml.html import FormElement
from lxml.html import InputElement
from lxml.html import MultipleSelectOptions
from lxml.html import SelectElement
from lxml.html import TextareaElement
from w3lib.html import strip_html5_whitespace
from scrapy.http.request import Request
from scrapy.http.response.text import TextResponse
from scrapy.utils.python import is_listlike, to_bytes
FormRequestTypeVar = TypeVar('FormRequestTypeVar', bound='FormRequest')
FormdataKVType = Tuple[str, Union[str, Iterable[str]]]
FormdataType = Optional[Union[dict, List[FormdataKVType]]]

class FormRequest(Request):
    valid_form_methods = ['GET', 'POST']

    def __init__(self, *args, formdata: FormdataType=None, **kwargs) -> None:
        if formdata and kwargs.get('method') is None:
            kwargs['method'] = 'POST'
        super().__init__(*args, **kwargs)
        if formdata:
            items = formdata.items() if isinstance(formdata, dict) else formdata
            form_query_str = _urlencode(items, self.encoding)
            if self.method == 'POST':
                self.headers.setdefault(b'Content-Type', b'application/x-www-form-urlencoded')
                self._set_body(form_query_str)
            else:
                self._set_url(urlunsplit(urlsplit(self.url)._replace(query=form_query_str)))

def _get_form(response: TextResponse, formname: Optional[str], formid: Optional[str], formnumber: int, formxpath: Optional[str]) -> FormElement:
    """Find the wanted form element within the given response."""
    pass

def _get_inputs(form: FormElement, formdata: FormdataType, dont_click: bool, clickdata: Optional[dict]) -> List[FormdataKVType]:
    """Return a list of key-value pairs for the inputs found in the given form."""
    pass

def _get_clickable(clickdata: Optional[dict], form: FormElement) -> Optional[Tuple[str, str]]:
    """
    Returns the clickable element specified in clickdata,
    if the latter is given. If not, it returns the first
    clickable element found
    """
    pass