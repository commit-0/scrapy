"""
DefaultHeaders downloader middleware

See documentation in docs/topics/downloader-middleware.rst
"""
from scrapy.utils.python import without_none_values

class DefaultHeadersMiddleware:

    def __init__(self, headers):
        self._headers = headers