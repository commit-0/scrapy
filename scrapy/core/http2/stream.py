import logging
from enum import Enum
from io import BytesIO
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple
from urllib.parse import urlparse
from h2.errors import ErrorCodes
from h2.exceptions import H2Error, ProtocolError, StreamClosedError
from hpack import HeaderTuple
from twisted.internet.defer import CancelledError, Deferred
from twisted.internet.error import ConnectionClosed
from twisted.python.failure import Failure
from twisted.web.client import ResponseFailed
from scrapy.http import Request
from scrapy.http.headers import Headers
from scrapy.responsetypes import responsetypes
if TYPE_CHECKING:
    from scrapy.core.http2.protocol import H2ClientProtocol
logger = logging.getLogger(__name__)

class InactiveStreamClosed(ConnectionClosed):
    """Connection was closed without sending request headers
    of the stream. This happens when a stream is waiting for other
    streams to close and connection is lost."""

    def __init__(self, request: Request) -> None:
        self.request = request

    def __str__(self) -> str:
        return f'InactiveStreamClosed: Connection was closed without sending the request {self.request!r}'

class InvalidHostname(H2Error):

    def __init__(self, request: Request, expected_hostname: str, expected_netloc: str) -> None:
        self.request = request
        self.expected_hostname = expected_hostname
        self.expected_netloc = expected_netloc

    def __str__(self) -> str:
        return f'InvalidHostname: Expected {self.expected_hostname} or {self.expected_netloc} in {self.request}'

class StreamCloseReason(Enum):
    ENDED = 1
    RESET = 2
    CONNECTION_LOST = 3
    MAXSIZE_EXCEEDED = 4
    CANCELLED = 5
    INACTIVE = 6
    INVALID_HOSTNAME = 7

class Stream:
    """Represents a single HTTP/2 Stream.

    Stream is a bidirectional flow of bytes within an established connection,
    which may carry one or more messages. Handles the transfer of HTTP Headers
    and Data frames.

    Role of this class is to
    1. Combine all the data frames
    """

    def __init__(self, stream_id: int, request: Request, protocol: 'H2ClientProtocol', download_maxsize: int=0, download_warnsize: int=0) -> None:
        """
        Arguments:
            stream_id -- Unique identifier for the stream within a single HTTP/2 connection
            request -- The HTTP request associated to the stream
            protocol -- Parent H2ClientProtocol instance
        """
        self.stream_id: int = stream_id
        self._request: Request = request
        self._protocol: 'H2ClientProtocol' = protocol
        self._download_maxsize = self._request.meta.get('download_maxsize', download_maxsize)
        self._download_warnsize = self._request.meta.get('download_warnsize', download_warnsize)
        self.metadata: Dict = {'request_content_length': 0 if self._request.body is None else len(self._request.body), 'request_sent': False, 'reached_warnsize': False, 'remaining_content_length': 0 if self._request.body is None else len(self._request.body), 'stream_closed_local': False, 'stream_closed_server': False}
        self._response: Dict = {'body': BytesIO(), 'flow_controlled_size': 0, 'headers': Headers({})}

        def _cancel(_) -> None:
            if self.metadata['request_sent']:
                self.reset_stream(StreamCloseReason.CANCELLED)
            else:
                self.close(StreamCloseReason.CANCELLED)
        self._deferred_response: Deferred = Deferred(_cancel)

    def __repr__(self) -> str:
        return f'Stream(id={self.stream_id!r})'

    @property
    def _log_warnsize(self) -> bool:
        """Checks if we have received data which exceeds the download warnsize
        and whether we have not already logged about it.

        Returns:
            True if both the above conditions hold true
            False if any of the conditions is false
        """
        pass

    def get_response(self) -> Deferred:
        """Simply return a Deferred which fires when response
        from the asynchronous request is available
        """
        pass

    def send_data(self) -> None:
        """Called immediately after the headers are sent. Here we send all the
        data as part of the request.

        If the content length is 0 initially then we end the stream immediately and
        wait for response data.

        Warning: Only call this method when stream not closed from client side
           and has initiated request already by sending HEADER frame. If not then
           stream will raise ProtocolError (raise by h2 state machine).
        """
        pass

    def receive_window_update(self) -> None:
        """Flow control window size was changed.
        Send data that earlier could not be sent as we were
        blocked behind the flow control.
        """
        pass

    def reset_stream(self, reason: StreamCloseReason=StreamCloseReason.RESET) -> None:
        """Close this stream by sending a RST_FRAME to the remote peer"""
        pass

    def close(self, reason: StreamCloseReason, errors: Optional[List[BaseException]]=None, from_protocol: bool=False) -> None:
        """Based on the reason sent we will handle each case."""
        pass

    def _fire_response_deferred(self) -> None:
        """Builds response from the self._response dict
        and fires the response deferred callback with the
        generated response instance"""
        pass