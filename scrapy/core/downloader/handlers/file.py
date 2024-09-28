from pathlib import Path
from w3lib.url import file_uri_to_path
from scrapy.responsetypes import responsetypes
from scrapy.utils.decorators import defers

class FileDownloadHandler:
    lazy = False