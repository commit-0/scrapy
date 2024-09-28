"""
An asynchronous FTP file download handler for scrapy which somehow emulates an http response.

FTP connection parameters are passed using the request meta field:
- ftp_user (required)
- ftp_password (required)
- ftp_passive (by default, enabled) sets FTP connection passive mode
- ftp_local_filename
        - If not given, file data will come in the response.body, as a normal scrapy Response,
        which will imply that the entire file will be on memory.
        - if given, file data will be saved in a local file with the given name
        This helps when downloading very big files to avoid memory issues. In addition, for
        convenience the local file name will also be given in the response body.

The status of the built html response will be, by default
- 200 in case of success
- 404 in case specified file was not found in the server (ftp code 550)

or raise corresponding ftp exception otherwise

The matching from server ftp command return codes to html response codes is defined in the
CODE_MAPPING attribute of the handler class. The key 'default' is used for any code
that is not explicitly present among the map keys. You may need to overwrite this
mapping if want a different behaviour than default.

In case of status 200 request, response.headers will come with two keys:
    'Local Filename' - with the value of the local filename if given
    'Size' - with size of the downloaded data
"""
import re
from io import BytesIO
from urllib.parse import unquote
from twisted.internet.protocol import ClientCreator, Protocol
from twisted.protocols.ftp import CommandFailed, FTPClient
from scrapy.http import Response
from scrapy.responsetypes import responsetypes
from scrapy.utils.httpobj import urlparse_cached
from scrapy.utils.python import to_bytes

class ReceivedDataProtocol(Protocol):

    def __init__(self, filename=None):
        self.__filename = filename
        self.body = open(filename, 'wb') if filename else BytesIO()
        self.size = 0
_CODE_RE = re.compile('\\d+')

class FTPDownloadHandler:
    lazy = False
    CODE_MAPPING = {'550': 404, 'default': 503}

    def __init__(self, settings):
        self.default_user = settings['FTP_USER']
        self.default_password = settings['FTP_PASSWORD']
        self.passive_mode = settings['FTP_PASSIVE_MODE']