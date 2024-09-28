"""Helper functions for working with signals"""
import collections.abc
import logging
from typing import Any as TypingAny
from typing import List, Tuple
from pydispatch.dispatcher import Anonymous, Any, disconnect, getAllReceivers, liveReceivers
from pydispatch.robustapply import robustApply
from twisted.internet.defer import Deferred, DeferredList
from twisted.python.failure import Failure
from scrapy.exceptions import StopDownload
from scrapy.utils.defer import maybeDeferred_coro
from scrapy.utils.log import failure_to_exc_info
logger = logging.getLogger(__name__)

def send_catch_log(signal: TypingAny=Any, sender: TypingAny=Anonymous, *arguments: TypingAny, **named: TypingAny) -> List[Tuple[TypingAny, TypingAny]]:
    """Like pydispatcher.robust.sendRobust but it also logs errors and returns
    Failures instead of exceptions.
    """
    pass

def send_catch_log_deferred(signal: TypingAny=Any, sender: TypingAny=Anonymous, *arguments: TypingAny, **named: TypingAny) -> Deferred:
    """Like send_catch_log but supports returning deferreds on signal handlers.
    Returns a deferred that gets fired once all signal handlers deferreds were
    fired.
    """
    pass

def disconnect_all(signal: TypingAny=Any, sender: TypingAny=Any) -> None:
    """Disconnect all signal handlers. Useful for cleaning up after running
    tests
    """
    pass