from __future__ import annotations
import os
import sys
from typing import Iterable, List, Optional, Tuple, cast
from twisted.internet.defer import Deferred
from twisted.internet.error import ProcessTerminated
from twisted.internet.protocol import ProcessProtocol
from twisted.python.failure import Failure

class ProcessTest:
    command = None
    prefix = [sys.executable, '-m', 'scrapy.cmdline']
    cwd = os.getcwd()

class TestProcessProtocol(ProcessProtocol):

    def __init__(self) -> None:
        self.deferred: Deferred = Deferred()
        self.out: bytes = b''
        self.err: bytes = b''
        self.exitcode: Optional[int] = None