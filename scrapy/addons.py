import logging
from typing import TYPE_CHECKING, Any, List
from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings
from scrapy.utils.conf import build_component_list
from scrapy.utils.misc import create_instance, load_object
if TYPE_CHECKING:
    from scrapy.crawler import Crawler
logger = logging.getLogger(__name__)

class AddonManager:
    """This class facilitates loading and storing :ref:`topics-addons`."""

    def __init__(self, crawler: 'Crawler') -> None:
        self.crawler: 'Crawler' = crawler
        self.addons: List[Any] = []

    def load_settings(self, settings: Settings) -> None:
        """Load add-ons and configurations from a settings object and apply them.

        This will load the add-on for every add-on path in the
        ``ADDONS`` setting and execute their ``update_settings`` methods.

        :param settings: The :class:`~scrapy.settings.Settings` object from             which to read the add-on configuration
        :type settings: :class:`~scrapy.settings.Settings`
        """
        pass