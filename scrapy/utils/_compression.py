import zlib
from io import BytesIO
from warnings import warn
from scrapy.exceptions import ScrapyDeprecationWarning
try:
    import brotli
except ImportError:
    pass
else:
    try:
        brotli.Decompressor.process
    except AttributeError:
        warn('You have brotlipy installed, and Scrapy will use it, but Scrapy support for brotlipy is deprecated and will stop working in a future version of Scrapy. brotlipy itself is deprecated, it has been superseded by brotlicffi (not currently supported by Scrapy). Please, uninstall brotlipy and install brotli instead. brotlipy has the same import name as brotli, so keeping both installed is strongly discouraged.', ScrapyDeprecationWarning)
try:
    import zstandard
except ImportError:
    pass
_CHUNK_SIZE = 65536

class _DecompressionMaxSizeExceeded(ValueError):
    pass