import logging
import re
import warnings
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.httpobj import urlparse_cached
logger = logging.getLogger(__name__)

class OffsiteMiddleware:

    def __init__(self, stats):
        self.stats = stats
        self.domains_seen = set()

    def get_host_regex(self, spider):
        """Override this method to implement a different offsite policy"""
        pass