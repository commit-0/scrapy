"""
Scrapy Telnet Console extension

See documentation in docs/topics/telnetconsole.rst
"""
import binascii
import logging
import os
import pprint
import traceback
from twisted.internet import protocol
try:
    from twisted.conch import manhole, telnet
    from twisted.conch.insults import insults
    TWISTED_CONCH_AVAILABLE = True
except (ImportError, SyntaxError):
    _TWISTED_CONCH_TRACEBACK = traceback.format_exc()
    TWISTED_CONCH_AVAILABLE = False
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.decorators import defers
from scrapy.utils.engine import print_engine_status
from scrapy.utils.reactor import listen_tcp
from scrapy.utils.trackref import print_live_refs
logger = logging.getLogger(__name__)
update_telnet_vars = object()

class TelnetConsole(protocol.ServerFactory):

    def __init__(self, crawler):
        if not crawler.settings.getbool('TELNETCONSOLE_ENABLED'):
            raise NotConfigured
        if not TWISTED_CONCH_AVAILABLE:
            raise NotConfigured('TELNETCONSOLE_ENABLED setting is True but required twisted modules failed to import:\n' + _TWISTED_CONCH_TRACEBACK)
        self.crawler = crawler
        self.noisy = False
        self.portrange = [int(x) for x in crawler.settings.getlist('TELNETCONSOLE_PORT')]
        self.host = crawler.settings['TELNETCONSOLE_HOST']
        self.username = crawler.settings['TELNETCONSOLE_USERNAME']
        self.password = crawler.settings['TELNETCONSOLE_PASSWORD']
        if not self.password:
            self.password = binascii.hexlify(os.urandom(8)).decode('utf8')
            logger.info('Telnet Password: %s', self.password)
        self.crawler.signals.connect(self.start_listening, signals.engine_started)
        self.crawler.signals.connect(self.stop_listening, signals.engine_stopped)