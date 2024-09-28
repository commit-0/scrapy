"""
Extension for processing data before they are exported to feeds.
"""
from bz2 import BZ2File
from gzip import GzipFile
from io import IOBase
from lzma import LZMAFile
from typing import Any, BinaryIO, Dict, List
from scrapy.utils.misc import load_object

class GzipPlugin:
    """
    Compresses received data using `gzip <https://en.wikipedia.org/wiki/Gzip>`_.

    Accepted ``feed_options`` parameters:

    - `gzip_compresslevel`
    - `gzip_mtime`
    - `gzip_filename`

    See :py:class:`gzip.GzipFile` for more info about parameters.
    """

    def __init__(self, file: BinaryIO, feed_options: Dict[str, Any]) -> None:
        self.file = file
        self.feed_options = feed_options
        compress_level = self.feed_options.get('gzip_compresslevel', 9)
        mtime = self.feed_options.get('gzip_mtime')
        filename = self.feed_options.get('gzip_filename')
        self.gzipfile = GzipFile(fileobj=self.file, mode='wb', compresslevel=compress_level, mtime=mtime, filename=filename)

class Bz2Plugin:
    """
    Compresses received data using `bz2 <https://en.wikipedia.org/wiki/Bzip2>`_.

    Accepted ``feed_options`` parameters:

    - `bz2_compresslevel`

    See :py:class:`bz2.BZ2File` for more info about parameters.
    """

    def __init__(self, file: BinaryIO, feed_options: Dict[str, Any]) -> None:
        self.file = file
        self.feed_options = feed_options
        compress_level = self.feed_options.get('bz2_compresslevel', 9)
        self.bz2file = BZ2File(filename=self.file, mode='wb', compresslevel=compress_level)

class LZMAPlugin:
    """
    Compresses received data using `lzma <https://en.wikipedia.org/wiki/Lempel–Ziv–Markov_chain_algorithm>`_.

    Accepted ``feed_options`` parameters:

    - `lzma_format`
    - `lzma_check`
    - `lzma_preset`
    - `lzma_filters`

    .. note::
        ``lzma_filters`` cannot be used in pypy version 7.3.1 and older.

    See :py:class:`lzma.LZMAFile` for more info about parameters.
    """

    def __init__(self, file: BinaryIO, feed_options: Dict[str, Any]) -> None:
        self.file = file
        self.feed_options = feed_options
        format = self.feed_options.get('lzma_format')
        check = self.feed_options.get('lzma_check', -1)
        preset = self.feed_options.get('lzma_preset')
        filters = self.feed_options.get('lzma_filters')
        self.lzmafile = LZMAFile(filename=self.file, mode='wb', format=format, check=check, preset=preset, filters=filters)

class PostProcessingManager(IOBase):
    """
    This will manage and use declared plugins to process data in a
    pipeline-ish way.
    :param plugins: all the declared plugins for the feed
    :type plugins: list
    :param file: final target file where the processed data will be written
    :type file: file like object
    """

    def __init__(self, plugins: List[Any], file: BinaryIO, feed_options: Dict[str, Any]) -> None:
        self.plugins = self._load_plugins(plugins)
        self.file = file
        self.feed_options = feed_options
        self.head_plugin = self._get_head_plugin()

    def write(self, data: bytes) -> int:
        """
        Uses all the declared plugins to process data first, then writes
        the processed data to target file.
        :param data: data passed to be written to target file
        :type data: bytes
        :return: returns number of bytes written
        :rtype: int
        """
        pass

    def close(self) -> None:
        """
        Close the target file along with all the plugins.
        """
        pass