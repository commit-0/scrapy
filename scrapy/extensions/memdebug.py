"""
MemoryDebugger extension

See documentation in docs/topics/extensions.rst
"""
import gc
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.trackref import live_refs

class MemoryDebugger:

    def __init__(self, stats):
        self.stats = stats