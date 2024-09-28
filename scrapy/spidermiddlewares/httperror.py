"""
HttpError Spider Middleware

See documentation in docs/topics/spider-middleware.rst
"""
import logging
from scrapy.exceptions import IgnoreRequest
logger = logging.getLogger(__name__)

class HttpError(IgnoreRequest):
    """A non-200 response was filtered"""

    def __init__(self, response, *args, **kwargs):
        self.response = response
        super().__init__(*args, **kwargs)

class HttpErrorMiddleware:

    def __init__(self, settings):
        self.handle_httpstatus_all = settings.getbool('HTTPERROR_ALLOW_ALL')
        self.handle_httpstatus_list = settings.getlist('HTTPERROR_ALLOWED_CODES')