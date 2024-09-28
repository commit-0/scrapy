import ipaddress
import itertools
import logging
from collections import deque
from ipaddress import IPv4Address, IPv6Address
from typing import Dict, List, Optional, Union
from h2.config import H2Configuration
from h2.connection import H2Connection
from h2.errors import ErrorCodes
from h2.events import ConnectionTerminated, DataReceived, Event, ResponseReceived, SettingsAcknowledged, StreamEnded, StreamReset, UnknownFrameReceived, WindowUpdated
from h2.exceptions import FrameTooLargeError, H2Error
from twisted.internet.defer import Deferred
from twisted.internet.error import TimeoutError
from twisted.internet.interfaces import IHandshakeListener, IProtocolNegotiationFactory
from twisted.internet.protocol import Factory, Protocol, connectionDone
from twisted.internet.ssl import Certificate
from twisted.protocols.policies import TimeoutMixin
from twisted.python.failure import Failure
from twisted.web.client import URI
from zope.interface import implementer
from scrapy.core.http2.stream import Stream, StreamCloseReason
from scrapy.http import Request
from scrapy.settings import Settings
from scrapy.spiders import Spider
logger = logging.getLogger(__name__)
PROTOCOL_NAME = b'h2'

class InvalidNegotiatedProtocol(H2Error):

    def __init__(self, negotiated_protocol: bytes) -> None:
        self.negotiated_protocol = negotiated_protocol

    def __str__(self) -> str:
        return f'Expected {PROTOCOL_NAME!r}, received {self.negotiated_protocol!r}'

class RemoteTerminatedConnection(H2Error):

    def __init__(self, remote_ip_address: Optional[Union[IPv4Address, IPv6Address]], event: ConnectionTerminated) -> None:
        self.remote_ip_address = remote_ip_address
        self.terminate_event = event

    def __str__(self) -> str:
        return f'Received GOAWAY frame from {self.remote_ip_address!r}'

class MethodNotAllowed405(H2Error):

    def __init__(self, remote_ip_address: Optional[Union[IPv4Address, IPv6Address]]) -> None:
        self.remote_ip_address = remote_ip_address

    def __str__(self) -> str:
        return f"Received 'HTTP/2.0 405 Method Not Allowed' from {self.remote_ip_address!r}"

@implementer(IHandshakeListener)
class H2ClientProtocol(Protocol, TimeoutMixin):
    IDLE_TIMEOUT = 240

    def __init__(self, uri: URI, settings: Settings, conn_lost_deferred: Deferred) -> None:
        """
        Arguments:
            uri -- URI of the base url to which HTTP/2 Connection will be made.
                uri is used to verify that incoming client requests have correct
                base URL.
            settings -- Scrapy project settings
            conn_lost_deferred -- Deferred fires with the reason: Failure to notify
                that connection was lost
        """
        self._conn_lost_deferred = conn_lost_deferred
        config = H2Configuration(client_side=True, header_encoding='utf-8')
        self.conn = H2Connection(config=config)
        self._stream_id_generator = itertools.count(start=1, step=2)
        self.streams: Dict[int, Stream] = {}
        self._pending_request_stream_pool: deque = deque()
        self._conn_lost_errors: List[BaseException] = []
        self.metadata: Dict = {'certificate': None, 'ip_address': None, 'uri': uri, 'default_download_maxsize': settings.getint('DOWNLOAD_MAXSIZE'), 'default_download_warnsize': settings.getint('DOWNLOAD_WARNSIZE'), 'active_streams': 0, 'settings_acknowledged': False}

    @property
    def h2_connected(self) -> bool:
        """Boolean to keep track of the connection status.
        This is used while initiating pending streams to make sure
        that we initiate stream only during active HTTP/2 Connection
        """
        pass

    @property
    def allowed_max_concurrent_streams(self) -> int:
        """We keep total two streams for client (sending data) and
        server side (receiving data) for a single request. To be safe
        we choose the minimum. Since this value can change in event
        RemoteSettingsChanged we make variable a property.
        """
        pass

    def _send_pending_requests(self) -> None:
        """Initiate all pending requests from the deque following FIFO
        We make sure that at any time {allowed_max_concurrent_streams}
        streams are active.
        """
        pass

    def pop_stream(self, stream_id: int) -> Stream:
        """Perform cleanup when a stream is closed"""
        pass

    def _new_stream(self, request: Request, spider: Spider) -> Stream:
        """Instantiates a new Stream object"""
        pass

    def _write_to_transport(self) -> None:
        """Write data to the underlying transport connection
        from the HTTP2 connection instance if any
        """
        pass

    def connectionMade(self) -> None:
        """Called by Twisted when the connection is established. We can start
        sending some data now: we should open with the connection preamble.
        """
        pass

    def _lose_connection_with_error(self, errors: List[BaseException]) -> None:
        """Helper function to lose the connection with the error sent as a
        reason"""
        pass

    def handshakeCompleted(self) -> None:
        """
        Close the connection if it's not made via the expected protocol
        """
        pass

    def _check_received_data(self, data: bytes) -> None:
        """Checks for edge cases where the connection to remote fails
        without raising an appropriate H2Error

        Arguments:
            data -- Data received from the remote
        """
        pass

    def timeoutConnection(self) -> None:
        """Called when the connection times out.
        We lose the connection with TimeoutError"""
        pass

    def connectionLost(self, reason: Failure=connectionDone) -> None:
        """Called by Twisted when the transport connection is lost.
        No need to write anything to transport here.
        """
        pass

    def _handle_events(self, events: List[Event]) -> None:
        """Private method which acts as a bridge between the events
        received from the HTTP/2 data and IH2EventsHandler

        Arguments:
            events -- A list of events that the remote peer triggered by sending data
        """
        pass

@implementer(IProtocolNegotiationFactory)
class H2ClientFactory(Factory):

    def __init__(self, uri: URI, settings: Settings, conn_lost_deferred: Deferred) -> None:
        self.uri = uri
        self.settings = settings
        self.conn_lost_deferred = conn_lost_deferred