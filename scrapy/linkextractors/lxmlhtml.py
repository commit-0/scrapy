"""
Link extractor based on lxml.html
"""
import logging
import operator
from functools import partial
from urllib.parse import urljoin, urlparse
from lxml import etree
from parsel.csstranslator import HTMLTranslator
from w3lib.html import strip_html5_whitespace
from w3lib.url import canonicalize_url, safe_url_string
from scrapy.link import Link
from scrapy.linkextractors import IGNORED_EXTENSIONS, _is_valid_url, _matches, _re_type, re
from scrapy.utils.misc import arg_to_iter, rel_has_nofollow
from scrapy.utils.python import unique as unique_list
from scrapy.utils.response import get_base_url
from scrapy.utils.url import url_has_any_extension, url_is_from_any_domain
logger = logging.getLogger(__name__)
XHTML_NAMESPACE = 'http://www.w3.org/1999/xhtml'
_collect_string_content = etree.XPath('string()')

class LxmlParserLinkExtractor:

    def __init__(self, tag='a', attr='href', process=None, unique=False, strip=True, canonicalized=False):
        self.scan_tag = tag if callable(tag) else partial(operator.eq, tag)
        self.scan_attr = attr if callable(attr) else partial(operator.eq, attr)
        self.process_attr = process if callable(process) else _identity
        self.unique = unique
        self.strip = strip
        self.link_key = operator.attrgetter('url') if canonicalized else _canonicalize_link_url

    def _process_links(self, links):
        """Normalize and filter extracted links

        The subclass should override it if necessary
        """
        pass

class LxmlLinkExtractor:
    _csstranslator = HTMLTranslator()

    def __init__(self, allow=(), deny=(), allow_domains=(), deny_domains=(), restrict_xpaths=(), tags=('a', 'area'), attrs=('href',), canonicalize=False, unique=True, process_value=None, deny_extensions=None, restrict_css=(), strip=True, restrict_text=None):
        tags, attrs = (set(arg_to_iter(tags)), set(arg_to_iter(attrs)))
        self.link_extractor = LxmlParserLinkExtractor(tag=partial(operator.contains, tags), attr=partial(operator.contains, attrs), unique=unique, process=process_value, strip=strip, canonicalized=not canonicalize)
        self.allow_res = [x if isinstance(x, _re_type) else re.compile(x) for x in arg_to_iter(allow)]
        self.deny_res = [x if isinstance(x, _re_type) else re.compile(x) for x in arg_to_iter(deny)]
        self.allow_domains = set(arg_to_iter(allow_domains))
        self.deny_domains = set(arg_to_iter(deny_domains))
        self.restrict_xpaths = tuple(arg_to_iter(restrict_xpaths))
        self.restrict_xpaths += tuple(map(self._csstranslator.css_to_xpath, arg_to_iter(restrict_css)))
        if deny_extensions is None:
            deny_extensions = IGNORED_EXTENSIONS
        self.canonicalize = canonicalize
        self.deny_extensions = {'.' + e for e in arg_to_iter(deny_extensions)}
        self.restrict_text = [x if isinstance(x, _re_type) else re.compile(x) for x in arg_to_iter(restrict_text)]

    def extract_links(self, response):
        """Returns a list of :class:`~scrapy.link.Link` objects from the
        specified :class:`response <scrapy.http.Response>`.

        Only links that match the settings passed to the ``__init__`` method of
        the link extractor are returned.

        Duplicate links are omitted if the ``unique`` attribute is set to ``True``,
        otherwise they are returned.
        """
        pass