"""
Item Exporters are used to export/serialize items into different formats.
"""
import csv
import io
import marshal
import pickle
import pprint
from collections.abc import Mapping
from xml.sax.saxutils import XMLGenerator
from itemadapter import ItemAdapter, is_item
from scrapy.item import Item
from scrapy.utils.python import is_listlike, to_bytes, to_unicode
from scrapy.utils.serialize import ScrapyJSONEncoder
__all__ = ['BaseItemExporter', 'PprintItemExporter', 'PickleItemExporter', 'CsvItemExporter', 'XmlItemExporter', 'JsonLinesItemExporter', 'JsonItemExporter', 'MarshalItemExporter']

class BaseItemExporter:

    def __init__(self, *, dont_fail=False, **kwargs):
        self._kwargs = kwargs
        self._configure(kwargs, dont_fail=dont_fail)

    def _configure(self, options, dont_fail=False):
        """Configure the exporter by popping options from the ``options`` dict.
        If dont_fail is set, it won't raise an exception on unexpected options
        (useful for using with keyword arguments in subclasses ``__init__`` methods)
        """
        pass

    def _get_serialized_fields(self, item, default_value=None, include_empty=None):
        """Return the fields to export as an iterable of tuples
        (name, serialized_value)
        """
        pass

class JsonLinesItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        super().__init__(dont_fail=True, **kwargs)
        self.file = file
        self._kwargs.setdefault('ensure_ascii', not self.encoding)
        self.encoder = ScrapyJSONEncoder(**self._kwargs)

class JsonItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        super().__init__(dont_fail=True, **kwargs)
        self.file = file
        json_indent = self.indent if self.indent is not None and self.indent > 0 else None
        self._kwargs.setdefault('indent', json_indent)
        self._kwargs.setdefault('ensure_ascii', not self.encoding)
        self.encoder = ScrapyJSONEncoder(**self._kwargs)
        self.first_item = True

class XmlItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        self.item_element = kwargs.pop('item_element', 'item')
        self.root_element = kwargs.pop('root_element', 'items')
        super().__init__(**kwargs)
        if not self.encoding:
            self.encoding = 'utf-8'
        self.xg = XMLGenerator(file, encoding=self.encoding)

class CsvItemExporter(BaseItemExporter):

    def __init__(self, file, include_headers_line=True, join_multivalued=',', errors=None, **kwargs):
        super().__init__(dont_fail=True, **kwargs)
        if not self.encoding:
            self.encoding = 'utf-8'
        self.include_headers_line = include_headers_line
        self.stream = io.TextIOWrapper(file, line_buffering=False, write_through=True, encoding=self.encoding, newline='', errors=errors)
        self.csv_writer = csv.writer(self.stream, **self._kwargs)
        self._headers_not_written = True
        self._join_multivalued = join_multivalued

class PickleItemExporter(BaseItemExporter):

    def __init__(self, file, protocol=4, **kwargs):
        super().__init__(**kwargs)
        self.file = file
        self.protocol = protocol

class MarshalItemExporter(BaseItemExporter):
    """Exports items in a Python-specific binary format (see
    :mod:`marshal`).

    :param file: The file-like object to use for exporting the data. Its
                 ``write`` method should accept :class:`bytes` (a disk file
                 opened in binary mode, a :class:`~io.BytesIO` object, etc)
    """

    def __init__(self, file, **kwargs):
        super().__init__(**kwargs)
        self.file = file

class PprintItemExporter(BaseItemExporter):

    def __init__(self, file, **kwargs):
        super().__init__(**kwargs)
        self.file = file

class PythonItemExporter(BaseItemExporter):
    """This is a base class for item exporters that extends
    :class:`BaseItemExporter` with support for nested items.

    It serializes items to built-in Python types, so that any serialization
    library (e.g. :mod:`json` or msgpack_) can be used on top of it.

    .. _msgpack: https://pypi.org/project/msgpack/
    """