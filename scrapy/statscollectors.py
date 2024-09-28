"""
Scrapy extension for collecting scraping stats
"""
import logging
import pprint
from typing import TYPE_CHECKING, Any, Dict, Optional
from scrapy import Spider
if TYPE_CHECKING:
    from scrapy.crawler import Crawler
logger = logging.getLogger(__name__)
StatsT = Dict[str, Any]

class StatsCollector:

    def __init__(self, crawler: 'Crawler'):
        self._dump: bool = crawler.settings.getbool('STATS_DUMP')
        self._stats: StatsT = {}

class MemoryStatsCollector(StatsCollector):

    def __init__(self, crawler: 'Crawler'):
        super().__init__(crawler)
        self.spider_stats: Dict[str, StatsT] = {}

class DummyStatsCollector(StatsCollector):
    pass