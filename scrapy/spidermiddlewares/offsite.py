"""
Offsite Spider Middleware

See documentation in docs/topics/spider-middleware.rst
"""
import logging
import re
import warnings
from scrapy import signals
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.http import Request
from scrapy.utils.httpobj import urlparse_cached
warnings.warn('The scrapy.spidermiddlewares.offsite module is deprecated, use scrapy.downloadermiddlewares.offsite instead.', ScrapyDeprecationWarning)
logger = logging.getLogger(__name__)

class OffsiteMiddleware:

    def __init__(self, stats):
        self.stats = stats

    def get_host_regex(self, spider):
        """Override this method to implement a different offsite policy"""
        pass

class URLWarning(Warning):
    pass

class PortWarning(Warning):
    pass