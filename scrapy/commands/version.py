import scrapy
from scrapy.commands import ScrapyCommand
from scrapy.utils.versions import scrapy_components_versions

class Command(ScrapyCommand):
    default_settings = {'LOG_ENABLED': False, 'SPIDER_LOADER_WARN_ONLY': True}