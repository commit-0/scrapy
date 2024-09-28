from __future__ import annotations
import traceback
import warnings
from collections import defaultdict
from types import ModuleType
from typing import TYPE_CHECKING, DefaultDict, Dict, List, Tuple, Type
from zope.interface import implementer
from scrapy import Request, Spider
from scrapy.interfaces import ISpiderLoader
from scrapy.settings import BaseSettings
from scrapy.utils.misc import walk_modules
from scrapy.utils.spider import iter_spider_classes
if TYPE_CHECKING:
    from typing_extensions import Self

@implementer(ISpiderLoader)
class SpiderLoader:
    """
    SpiderLoader is a class which locates and loads spiders
    in a Scrapy project.
    """

    def __init__(self, settings: BaseSettings):
        self.spider_modules: List[str] = settings.getlist('SPIDER_MODULES')
        self.warn_only: bool = settings.getbool('SPIDER_LOADER_WARN_ONLY')
        self._spiders: Dict[str, Type[Spider]] = {}
        self._found: DefaultDict[str, List[Tuple[str, str]]] = defaultdict(list)
        self._load_all_spiders()

    def load(self, spider_name: str) -> Type[Spider]:
        """
        Return the Spider class for the given spider name. If the spider
        name is not found, raise a KeyError.
        """
        pass

    def find_by_request(self, request: Request) -> List[str]:
        """
        Return the list of spider names that can handle the given request.
        """
        pass

    def list(self) -> List[str]:
        """
        Return a list with the names of all spiders available in the project.
        """
        pass