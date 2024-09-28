"""
MemoryUsage extension

See documentation in docs/topics/extensions.rst
"""
import logging
import socket
import sys
from importlib import import_module
from pprint import pformat
from twisted.internet import task
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.mail import MailSender
from scrapy.utils.engine import get_engine_status
logger = logging.getLogger(__name__)

class MemoryUsage:

    def __init__(self, crawler):
        if not crawler.settings.getbool('MEMUSAGE_ENABLED'):
            raise NotConfigured
        try:
            self.resource = import_module('resource')
        except ImportError:
            raise NotConfigured
        self.crawler = crawler
        self.warned = False
        self.notify_mails = crawler.settings.getlist('MEMUSAGE_NOTIFY_MAIL')
        self.limit = crawler.settings.getint('MEMUSAGE_LIMIT_MB') * 1024 * 1024
        self.warning = crawler.settings.getint('MEMUSAGE_WARNING_MB') * 1024 * 1024
        self.check_interval = crawler.settings.getfloat('MEMUSAGE_CHECK_INTERVAL_SECONDS')
        self.mail = MailSender.from_settings(crawler.settings)
        crawler.signals.connect(self.engine_started, signal=signals.engine_started)
        crawler.signals.connect(self.engine_stopped, signal=signals.engine_stopped)

    def _send_report(self, rcpts, subject):
        """send notification mail with some additional useful info"""
        pass