"""
Images Pipeline

See documentation in topics/media-pipeline.rst
"""
import functools
import hashlib
import warnings
from contextlib import suppress
from io import BytesIO
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem, NotConfigured, ScrapyDeprecationWarning
from scrapy.http import Request
from scrapy.http.request import NO_CALLBACK
from scrapy.pipelines.files import FileException, FilesPipeline
from scrapy.settings import Settings
from scrapy.utils.misc import md5sum
from scrapy.utils.python import get_func_args, to_bytes

class NoimagesDrop(DropItem):
    """Product with no images exception"""

    def __init__(self, *args, **kwargs):
        warnings.warn('The NoimagesDrop class is deprecated', category=ScrapyDeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)

class ImageException(FileException):
    """General image error exception"""

class ImagesPipeline(FilesPipeline):
    """Abstract pipeline that implement the image thumbnail generation logic"""
    MEDIA_NAME = 'image'
    MIN_WIDTH = 0
    MIN_HEIGHT = 0
    EXPIRES = 90
    THUMBS = {}
    DEFAULT_IMAGES_URLS_FIELD = 'image_urls'
    DEFAULT_IMAGES_RESULT_FIELD = 'images'

    def __init__(self, store_uri, download_func=None, settings=None):
        try:
            from PIL import Image
            self._Image = Image
        except ImportError:
            raise NotConfigured('ImagesPipeline requires installing Pillow 4.0.0 or later')
        super().__init__(store_uri, settings=settings, download_func=download_func)
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)
        resolve = functools.partial(self._key_for_pipe, base_class_name='ImagesPipeline', settings=settings)
        self.expires = settings.getint(resolve('IMAGES_EXPIRES'), self.EXPIRES)
        if not hasattr(self, 'IMAGES_RESULT_FIELD'):
            self.IMAGES_RESULT_FIELD = self.DEFAULT_IMAGES_RESULT_FIELD
        if not hasattr(self, 'IMAGES_URLS_FIELD'):
            self.IMAGES_URLS_FIELD = self.DEFAULT_IMAGES_URLS_FIELD
        self.images_urls_field = settings.get(resolve('IMAGES_URLS_FIELD'), self.IMAGES_URLS_FIELD)
        self.images_result_field = settings.get(resolve('IMAGES_RESULT_FIELD'), self.IMAGES_RESULT_FIELD)
        self.min_width = settings.getint(resolve('IMAGES_MIN_WIDTH'), self.MIN_WIDTH)
        self.min_height = settings.getint(resolve('IMAGES_MIN_HEIGHT'), self.MIN_HEIGHT)
        self.thumbs = settings.get(resolve('IMAGES_THUMBS'), self.THUMBS)
        self._deprecated_convert_image = None