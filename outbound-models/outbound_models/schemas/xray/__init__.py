import msgspec
from typing import Literal

from .protocols import AnyProtocol
from .transports.grpc import GrpcTransport
from .transports.ws import WebsocketTransport
from .transports.hysteria2 import Hysteria2Transport

NetworkValues = Literal["raw", "tcp", "xhttp", "mkcp", "grpc", "websocket", "httpupgrade", "hysteria"]
SecurityValues = Literal["none", "reality", "tls"]


class StreamSettings(msgspec.Struct, rename="camel"):
    network: NetworkValues
    grpc_settings: GrpcTransport | None = None
    ws_settings: WebsocketTransport | None = None
    hysteria_settings: Hysteria2Transport | None = None
    security: SecurityValues | None = None


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
