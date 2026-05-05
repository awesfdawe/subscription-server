from pydantic import BaseModel
from typing import Optional, Union

from .protocols.vless import VlessSettings
from .transports.ws import WsTransport
from .transports.grpc import GrpcTransport
from .transports.xhttp import XhttpTransport
from .transports.tcp import TcpTransport

TransportConfig = Union[WsTransport, GrpcTransport, TcpTransport, XhttpTransport]


class ProxyConfig(BaseModel):
    protocol_settings: VlessSettings
    transport: Optional[TransportConfig] = None
