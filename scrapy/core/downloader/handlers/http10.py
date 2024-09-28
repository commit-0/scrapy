"""Download handlers for http and https schemes
"""
from scrapy.utils.misc import create_instance, load_object
from scrapy.utils.python import to_unicode

class HTTP10DownloadHandler:
    lazy = False

    def __init__(self, settings, crawler=None):
        self.HTTPClientFactory = load_object(settings['DOWNLOADER_HTTPCLIENTFACTORY'])
        self.ClientContextFactory = load_object(settings['DOWNLOADER_CLIENTCONTEXTFACTORY'])
        self._settings = settings
        self._crawler = crawler

    def download_request(self, request, spider):
        """Return a deferred for the HTTP download"""
        pass