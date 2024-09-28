import logging
from urllib.parse import urljoin, urlparse
from w3lib.url import safe_url_string
from scrapy.exceptions import IgnoreRequest, NotConfigured
from scrapy.http import HtmlResponse
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.response import get_meta_refresh
logger = logging.getLogger(__name__)

class BaseRedirectMiddleware:
    enabled_setting = 'REDIRECT_ENABLED'

    def __init__(self, settings):
        if not settings.getbool(self.enabled_setting):
            raise NotConfigured
        self.max_redirect_times = settings.getint('REDIRECT_MAX_TIMES')
        self.priority_adjust = settings.getint('REDIRECT_PRIORITY_ADJUST')

class RedirectMiddleware(BaseRedirectMiddleware):
    """
    Handle redirection of requests based on response status
    and meta-refresh html tag.
    """

class MetaRefreshMiddleware(BaseRedirectMiddleware):
    enabled_setting = 'METAREFRESH_ENABLED'

    def __init__(self, settings):
        super().__init__(settings)
        self._ignore_tags = settings.getlist('METAREFRESH_IGNORE_TAGS')
        self._maxdelay = settings.getint('METAREFRESH_MAXDELAY')