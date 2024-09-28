from __future__ import annotations
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Set
from warnings import warn
from twisted.internet.defer import Deferred
from scrapy.http.request import Request
from scrapy.settings import BaseSettings
from scrapy.spiders import Spider
from scrapy.utils.deprecate import ScrapyDeprecationWarning
from scrapy.utils.job import job_dir
from scrapy.utils.request import RequestFingerprinter, RequestFingerprinterProtocol, referer_str
if TYPE_CHECKING:
    from typing_extensions import Self
    from scrapy.crawler import Crawler

class BaseDupeFilter:

    def log(self, request: Request, spider: Spider) -> None:
        """Log that a request has been filtered"""
        pass

class RFPDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""

    def __init__(self, path: Optional[str]=None, debug: bool=False, *, fingerprinter: Optional[RequestFingerprinterProtocol]=None) -> None:
        self.file = None
        self.fingerprinter: RequestFingerprinterProtocol = fingerprinter or RequestFingerprinter()
        self.fingerprints: Set[str] = set()
        self.logdupes = True
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        if path:
            self.file = Path(path, 'requests.seen').open('a+', encoding='utf-8')
            self.file.seek(0)
            self.fingerprints.update((x.rstrip() for x in self.file))