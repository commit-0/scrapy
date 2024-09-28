from collections.abc import Mapping
from w3lib.http import headers_dict_to_raw
from scrapy.utils.datatypes import CaseInsensitiveDict, CaselessDict
from scrapy.utils.python import to_unicode

class Headers(CaselessDict):
    """Case insensitive http headers dictionary"""

    def __init__(self, seq=None, encoding='utf-8'):
        self.encoding = encoding
        super().__init__(seq)

    def normkey(self, key):
        """Normalize key to bytes"""
        pass

    def normvalue(self, value):
        """Normalize values to bytes"""
        pass

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)[-1]
        except IndexError:
            return None

    def to_unicode_dict(self):
        """Return headers as a CaselessDict with unicode keys
        and unicode values. Multiple values are joined with ','.
        """
        pass

    def __copy__(self):
        return self.__class__(self)
    copy = __copy__