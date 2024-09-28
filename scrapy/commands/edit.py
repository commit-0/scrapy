import os
import sys
from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError

class Command(ScrapyCommand):
    requires_project = True
    default_settings = {'LOG_ENABLED': False}