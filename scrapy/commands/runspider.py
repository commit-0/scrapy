import sys
from importlib import import_module
from os import PathLike
from pathlib import Path
from types import ModuleType
from typing import Union
from scrapy.commands import BaseRunSpiderCommand
from scrapy.exceptions import UsageError
from scrapy.utils.spider import iter_spider_classes

class Command(BaseRunSpiderCommand):
    requires_project = False
    default_settings = {'SPIDER_LOADER_WARN_ONLY': True}