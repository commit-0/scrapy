from twisted.web import http
from scrapy.exceptions import NotConfigured
from scrapy.utils.python import global_object_name, to_bytes
from scrapy.utils.request import request_httprepr

class DownloaderStats:

    def __init__(self, stats):
        self.stats = stats