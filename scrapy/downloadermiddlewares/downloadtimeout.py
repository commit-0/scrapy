"""
Download timeout middleware

See documentation in docs/topics/downloader-middleware.rst
"""
from scrapy import signals

class DownloadTimeoutMiddleware:

    def __init__(self, timeout=180):
        self._timeout = timeout