import struct
from gzip import GzipFile
from io import BytesIO
from scrapy.http import Response
from ._compression import _CHUNK_SIZE, _DecompressionMaxSizeExceeded

def gunzip(data: bytes, *, max_size: int=0) -> bytes:
    """Gunzip the given data and return as much data as possible.

    This is resilient to CRC checksum errors.
    """
    pass