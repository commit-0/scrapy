"""Helper functions for working with templates"""
import re
import string
from os import PathLike
from pathlib import Path
from typing import Any, Union
CAMELCASE_INVALID_CHARS = re.compile('[^a-zA-Z\\d]')

def string_camelcase(string: str) -> str:
    """Convert a word  to its CamelCase version and remove invalid chars

    >>> string_camelcase('lost-pound')
    'LostPound'

    >>> string_camelcase('missing_images')
    'MissingImages'

    """
    pass