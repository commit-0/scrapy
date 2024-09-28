import json
from scrapy.commands import ScrapyCommand
from scrapy.settings import BaseSettings

class Command(ScrapyCommand):
    requires_project = False
    default_settings = {'LOG_ENABLED': False, 'SPIDER_LOADER_WARN_ONLY': True}