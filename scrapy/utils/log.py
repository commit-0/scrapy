from __future__ import annotations
import logging
import sys
import warnings
from logging.config import dictConfig
from types import TracebackType
from typing import TYPE_CHECKING, Any, List, MutableMapping, Optional, Tuple, Type, Union, cast
from twisted.python import log as twisted_log
from twisted.python.failure import Failure
import scrapy
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy.settings import Settings
from scrapy.utils.versions import scrapy_components_versions
if TYPE_CHECKING:
    from scrapy.crawler import Crawler
logger = logging.getLogger(__name__)

def failure_to_exc_info(failure: Failure) -> Optional[Tuple[Type[BaseException], BaseException, Optional[TracebackType]]]:
    """Extract exc_info from Failure instances"""
    pass

class TopLevelFormatter(logging.Filter):
    """Keep only top level loggers's name (direct children from root) from
    records.

    This filter will replace Scrapy loggers' names with 'scrapy'. This mimics
    the old Scrapy log behaviour and helps shortening long names.

    Since it can't be set for just one logger (it won't propagate for its
    children), it's going to be set in the root handler, with a parametrized
    ``loggers`` list where it should act.
    """

    def __init__(self, loggers: Optional[List[str]]=None):
        self.loggers: List[str] = loggers or []
DEFAULT_LOGGING = {'version': 1, 'disable_existing_loggers': False, 'loggers': {'filelock': {'level': 'ERROR'}, 'hpack': {'level': 'ERROR'}, 'scrapy': {'level': 'DEBUG'}, 'twisted': {'level': 'ERROR'}}}

def configure_logging(settings: Union[Settings, dict, None]=None, install_root_handler: bool=True) -> None:
    """
    Initialize logging defaults for Scrapy.

    :param settings: settings used to create and configure a handler for the
        root logger (default: None).
    :type settings: dict, :class:`~scrapy.settings.Settings` object or ``None``

    :param install_root_handler: whether to install root logging handler
        (default: True)
    :type install_root_handler: bool

    This function does:

    - Route warnings and twisted logging through Python standard logging
    - Assign DEBUG and ERROR level to Scrapy and Twisted loggers respectively
    - Route stdout to log if LOG_STDOUT setting is True

    When ``install_root_handler`` is True (default), this function also
    creates a handler for the root logger according to given settings
    (see :ref:`topics-logging-settings`). You can override default options
    using ``settings`` argument. When ``settings`` is empty or None, defaults
    are used.
    """
    pass
_scrapy_root_handler: Optional[logging.Handler] = None

def _get_handler(settings: Settings) -> logging.Handler:
    """Return a log handler object according to settings"""
    pass

class StreamLogger:
    """Fake file-like stream object that redirects writes to a logger instance

    Taken from:
        https://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/
    """

    def __init__(self, logger: logging.Logger, log_level: int=logging.INFO):
        self.logger: logging.Logger = logger
        self.log_level: int = log_level
        self.linebuf: str = ''

class LogCounterHandler(logging.Handler):
    """Record log levels count into a crawler stats"""

    def __init__(self, crawler: Crawler, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.crawler: Crawler = crawler

def logformatter_adapter(logkws: dict) -> Tuple[int, str, dict]:
    """
    Helper that takes the dictionary output from the methods in LogFormatter
    and adapts it into a tuple of positional arguments for logger.log calls,
    handling backward compatibility as well.
    """
    pass

class SpiderLoggerAdapter(logging.LoggerAdapter):

    def process(self, msg: str, kwargs: MutableMapping[str, Any]) -> Tuple[str, MutableMapping[str, Any]]:
        """Method that augments logging with additional 'extra' data"""
        pass