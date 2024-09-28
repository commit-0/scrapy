import os
import warnings
from importlib import import_module
from pathlib import Path
from scrapy.exceptions import NotConfigured
from scrapy.settings import Settings
from scrapy.utils.conf import closest_scrapy_cfg, get_config, init_env
ENVVAR = 'SCRAPY_SETTINGS_MODULE'
DATADIR_CFG_SECTION = 'datadir'

def project_data_dir(project: str='default') -> str:
    """Return the current project data dir, creating it if it doesn't exist"""
    pass

def data_path(path: str, createdir: bool=False) -> str:
    """
    Return the given path joined with the .scrapy data directory.
    If given an absolute path, return it unmodified.
    """
    pass