"""
Url Length Spider Middleware

See documentation in docs/topics/spider-middleware.rst
"""
import logging
from scrapy.exceptions import NotConfigured
from scrapy.http import Request
logger = logging.getLogger(__name__)

class UrlLengthMiddleware:

    def __init__(self, maxlength):
        self.maxlength = maxlength