from __future__ import annotations
import logging
import os
from typing import TYPE_CHECKING, Any, Dict, Optional, Union
from twisted.python.failure import Failure
from scrapy import Request, Spider
from scrapy.http import Response
from scrapy.utils.request import referer_str
if TYPE_CHECKING:
    from typing_extensions import Self
    from scrapy.crawler import Crawler
SCRAPEDMSG = 'Scraped from %(src)s' + os.linesep + '%(item)s'
DROPPEDMSG = 'Dropped: %(exception)s' + os.linesep + '%(item)s'
CRAWLEDMSG = 'Crawled (%(status)s) %(request)s%(request_flags)s (referer: %(referer)s)%(response_flags)s'
ITEMERRORMSG = 'Error processing %(item)s'
SPIDERERRORMSG = 'Spider error processing %(request)s (referer: %(referer)s)'
DOWNLOADERRORMSG_SHORT = 'Error downloading %(request)s'
DOWNLOADERRORMSG_LONG = 'Error downloading %(request)s: %(errmsg)s'

class LogFormatter:
    """Class for generating log messages for different actions.

    All methods must return a dictionary listing the parameters ``level``, ``msg``
    and ``args`` which are going to be used for constructing the log message when
    calling ``logging.log``.

    Dictionary keys for the method outputs:

    *   ``level`` is the log level for that action, you can use those from the
        `python logging library <https://docs.python.org/3/library/logging.html>`_ :
        ``logging.DEBUG``, ``logging.INFO``, ``logging.WARNING``, ``logging.ERROR``
        and ``logging.CRITICAL``.
    *   ``msg`` should be a string that can contain different formatting placeholders.
        This string, formatted with the provided ``args``, is going to be the long message
        for that action.
    *   ``args`` should be a tuple or dict with the formatting placeholders for ``msg``.
        The final log message is computed as ``msg % args``.

    Users can define their own ``LogFormatter`` class if they want to customize how
    each action is logged or if they want to omit it entirely. In order to omit
    logging an action the method must return ``None``.

    Here is an example on how to create a custom log formatter to lower the severity level of
    the log message when an item is dropped from the pipeline::

            class PoliteLogFormatter(logformatter.LogFormatter):
                def dropped(self, item, exception, response, spider):
                    return {
                        'level': logging.INFO, # lowering the level from logging.WARNING
                        'msg': "Dropped: %(exception)s" + os.linesep + "%(item)s",
                        'args': {
                            'exception': exception,
                            'item': item,
                        }
                    }
    """

    def crawled(self, request: Request, response: Response, spider: Spider) -> dict:
        """Logs a message when the crawler finds a webpage."""
        pass

    def scraped(self, item: Any, response: Union[Response, Failure], spider: Spider) -> dict:
        """Logs a message when an item is scraped by a spider."""
        pass

    def dropped(self, item: Any, exception: BaseException, response: Response, spider: Spider) -> dict:
        """Logs a message when an item is dropped while it is passing through the item pipeline."""
        pass

    def item_error(self, item: Any, exception: BaseException, response: Response, spider: Spider) -> dict:
        """Logs a message when an item causes an error while it is passing
        through the item pipeline.

        .. versionadded:: 2.0
        """
        pass

    def spider_error(self, failure: Failure, request: Request, response: Union[Response, Failure], spider: Spider) -> dict:
        """Logs an error message from a spider.

        .. versionadded:: 2.0
        """
        pass

    def download_error(self, failure: Failure, request: Request, spider: Spider, errmsg: Optional[str]=None) -> dict:
        """Logs a download error message from a spider (typically coming from
        the engine).

        .. versionadded:: 2.0
        """
        pass