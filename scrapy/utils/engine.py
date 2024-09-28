"""Some debugging functions for working with the Scrapy engine"""
from time import time
from typing import TYPE_CHECKING, Any, List, Tuple
if TYPE_CHECKING:
    from scrapy.core.engine import ExecutionEngine

def get_engine_status(engine: 'ExecutionEngine') -> List[Tuple[str, Any]]:
    """Return a report of the current engine status"""
    pass