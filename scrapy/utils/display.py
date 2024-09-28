"""
pprint and pformat wrappers with colorization support
"""
import ctypes
import platform
import sys
from pprint import pformat as pformat_
from typing import Any
from packaging.version import Version as parse_version