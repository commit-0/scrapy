from w3lib.url import parse_data_uri
from scrapy.http import TextResponse
from scrapy.responsetypes import responsetypes
from scrapy.utils.decorators import defers

class DataURIDownloadHandler:
    lazy = False