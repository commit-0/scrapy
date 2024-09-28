import logging
from datetime import datetime, timezone
from twisted.internet import task
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.serialize import ScrapyJSONEncoder
logger = logging.getLogger(__name__)

class PeriodicLog:
    """Log basic scraping stats periodically"""

    def __init__(self, stats, interval=60.0, ext_stats={}, ext_delta={}, ext_timing_enabled=False):
        self.stats = stats
        self.interval = interval
        self.multiplier = 60.0 / self.interval
        self.task = None
        self.encoder = ScrapyJSONEncoder(sort_keys=True, indent=4)
        self.ext_stats_enabled = bool(ext_stats)
        self.ext_stats_include = ext_stats.get('include', [])
        self.ext_stats_exclude = ext_stats.get('exclude', [])
        self.ext_delta_enabled = bool(ext_delta)
        self.ext_delta_include = ext_delta.get('include', [])
        self.ext_delta_exclude = ext_delta.get('exclude', [])
        self.ext_timing_enabled = ext_timing_enabled