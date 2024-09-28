"""
The Extension Manager

See documentation in docs/topics/extensions.rst
"""
from scrapy.middleware import MiddlewareManager
from scrapy.utils.conf import build_component_list

class ExtensionManager(MiddlewareManager):
    component_name = 'extension'