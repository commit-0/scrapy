import numbers
import os
import sys
import warnings
from configparser import ConfigParser
from operator import itemgetter
from pathlib import Path
from typing import Any, Callable, Collection, Dict, Iterable, List, Mapping, MutableMapping, Optional, Union
from scrapy.exceptions import ScrapyDeprecationWarning, UsageError
from scrapy.settings import BaseSettings
from scrapy.utils.deprecate import update_classpath
from scrapy.utils.python import without_none_values

def build_component_list(compdict: MutableMapping[Any, Any], custom: Any=None, convert: Callable[[Any], Any]=update_classpath) -> List[Any]:
    """Compose a component list from a { class: order } dictionary."""
    pass

def arglist_to_dict(arglist: List[str]) -> Dict[str, str]:
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    pass

def closest_scrapy_cfg(path: Union[str, os.PathLike]='.', prevpath: Optional[Union[str, os.PathLike]]=None) -> str:
    """Return the path to the closest scrapy.cfg file by traversing the current
    directory and its parents
    """
    pass

def init_env(project: str='default', set_syspath: bool=True) -> None:
    """Initialize environment to use command-line tool from inside a project
    dir. This sets the Scrapy settings module and modifies the Python path to
    be able to locate the project module.
    """
    pass

def get_config(use_closest: bool=True) -> ConfigParser:
    """Get Scrapy config file as a ConfigParser"""
    pass

def feed_process_params_from_cli(settings: BaseSettings, output: List[str], output_format: Optional[str]=None, overwrite_output: Optional[List[str]]=None) -> Dict[str, Dict[str, Any]]:
    """
    Receives feed export params (from the 'crawl' or 'runspider' commands),
    checks for inconsistencies in their quantities and returns a dictionary
    suitable to be used as the FEEDS setting.
    """
    pass