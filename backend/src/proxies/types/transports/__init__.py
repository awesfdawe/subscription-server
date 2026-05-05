from typing import Union
from .tcp import TcpTransport
from .grpc import GrpcTransport
from .ws import WsTransport
from .xhttp import XhttpTransport

TransportConfig = Union[TcpTransport, GrpcTransport, WsTransport, XhttpTransport]
