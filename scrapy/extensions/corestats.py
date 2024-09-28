"""
Extension for collecting core stats like items scraped and start/finish times
"""
from datetime import datetime, timezone
from scrapy import signals

class CoreStats:

    def __init__(self, stats):
        self.stats = stats
        self.start_time = None