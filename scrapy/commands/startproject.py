import os
import re
import string
from importlib.util import find_spec
from pathlib import Path
from shutil import copy2, copystat, ignore_patterns, move
from stat import S_IWUSR as OWNER_WRITE_PERMISSION
import scrapy
from scrapy.commands import ScrapyCommand
from scrapy.exceptions import UsageError
from scrapy.utils.template import render_templatefile, string_camelcase
TEMPLATES_TO_RENDER = (('scrapy.cfg',), ('${project_name}', 'settings.py.tmpl'), ('${project_name}', 'items.py.tmpl'), ('${project_name}', 'pipelines.py.tmpl'), ('${project_name}', 'middlewares.py.tmpl'))
IGNORE = ignore_patterns('*.pyc', '__pycache__', '.svn')

class Command(ScrapyCommand):
    requires_project = False
    default_settings = {'LOG_ENABLED': False, 'SPIDER_LOADER_WARN_ONLY': True}

    def _copytree(self, src: Path, dst: Path):
        """
        Since the original function always creates the directory, to resolve
        the issue a new function had to be created. It's a simple copy and
        was reduced for this case.

        More info at:
        https://github.com/scrapy/scrapy/pull/2005
        """
        pass