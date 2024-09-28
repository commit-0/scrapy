import subprocess
import sys
import time
from urllib.parse import urlencode
import scrapy
from scrapy.commands import ScrapyCommand
from scrapy.linkextractors import LinkExtractor

class Command(ScrapyCommand):
    default_settings = {'LOG_LEVEL': 'INFO', 'LOGSTATS_INTERVAL': 1, 'CLOSESPIDER_TIMEOUT': 10}

class _BenchServer:

    def __enter__(self):
        from scrapy.utils.test import get_testenv
        pargs = [sys.executable, '-u', '-m', 'scrapy.utils.benchserver']
        self.proc = subprocess.Popen(pargs, stdout=subprocess.PIPE, env=get_testenv())
        self.proc.stdout.readline()

    def __exit__(self, exc_type, exc_value, traceback):
        self.proc.kill()
        self.proc.wait()
        time.sleep(0.2)

class _BenchSpider(scrapy.Spider):
    """A spider that follows all links"""
    name = 'follow'
    total = 10000
    show = 20
    baseurl = 'http://localhost:8998'
    link_extractor = LinkExtractor()