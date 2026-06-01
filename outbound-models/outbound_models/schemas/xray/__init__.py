import msgspec
from typing import Literal

from .protocols import AnyProtocol
from .transports.grpc import GrpcTransportXray
from .transports.ws import WebsocketTransportXray
from .transports.hysteria2 import Hysteria2TransportXray
from .security.reality import RealitySecurityXray
from .security.tls import TlsSecurityXray

NetworkValues = Literal["raw", "tcp", "xhttp", "mkcp", "grpc", "websocket", "httpupgrade", "hysteria"]
SecurityValues = Literal["none", "reality", "tls"]


class StreamSettings(msgspec.Struct, rename="camel"):
    network: NetworkValues
    grpc_settings: GrpcTransportXray | None = None
    ws_settings: WebsocketTransportXray | None = None
    hysteria_settings: Hysteria2TransportXray | None = None
    security: SecurityValues | None = None
    reality_settings: RealitySecurityXray | None = None
    tls_settings: TlsSecurityXray | None = None


XrayProtocols = Literal[
    "vless",
    "vmess",
    "wireguard",
    "hysteria",
    "trojan",
    "socks",
    "shadowsocks",
    "loopback",
    "http",
    "freedom",
    "dns",
    "blackhole",
]


class XrayConfig(msgspec.Struct, rename="camel"):
    protocol: XrayProtocols
    tag: str
    settings: AnyProtocol
    stream_settings: StreamSettings | None = None
