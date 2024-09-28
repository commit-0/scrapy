"""
Depth Spider Middleware

See documentation in docs/topics/spider-middleware.rst
"""
import logging
from scrapy.http import Request
logger = logging.getLogger(__name__)

class DepthMiddleware:

    def __init__(self, maxdepth, stats, verbose_stats=False, prio=1):
        self.maxdepth = maxdepth
        self.stats = stats
        self.verbose_stats = verbose_stats
        self.prio = prio