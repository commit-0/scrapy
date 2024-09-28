from scrapy.commands import ScrapyCommand

class Command(ScrapyCommand):
    requires_project = True
    default_settings = {'LOG_ENABLED': False}