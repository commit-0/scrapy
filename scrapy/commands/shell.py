"""
Scrapy Shell

See documentation in docs/topics/shell.rst
"""
from argparse import Namespace
from threading import Thread
from typing import List, Type
from scrapy import Spider
from scrapy.commands import ScrapyCommand
from scrapy.http import Request
from scrapy.shell import Shell
from scrapy.utils.spider import DefaultSpider, spidercls_for_request
from scrapy.utils.url import guess_scheme

class Command(ScrapyCommand):
    requires_project = False
    default_settings = {'KEEP_ALIVE': True, 'LOGSTATS_INTERVAL': 0, 'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter'}

    def update_vars(self, vars):
        """You can use this function to update the Scrapy objects that will be
        available in the shell
        """
        pass