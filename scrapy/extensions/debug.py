"""
Extensions for debugging Scrapy

See documentation in docs/topics/extensions.rst
"""
import logging
import signal
import sys
import threading
import traceback
from pdb import Pdb
from scrapy.utils.engine import format_engine_status
from scrapy.utils.trackref import format_live_refs
logger = logging.getLogger(__name__)

class StackTraceDump:

    def __init__(self, crawler=None):
        self.crawler = crawler
        try:
            signal.signal(signal.SIGUSR2, self.dump_stacktrace)
            signal.signal(signal.SIGQUIT, self.dump_stacktrace)
        except AttributeError:
            pass

class Debugger:

    def __init__(self):
        try:
            signal.signal(signal.SIGUSR2, self._enter_debugger)
        except AttributeError:
            pass