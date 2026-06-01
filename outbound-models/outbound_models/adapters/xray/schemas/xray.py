import msgspec
from typing import Any, Literal


NetworkValues = Literal["raw", "tcp", "xhttp", "mkcp", "grpc", "websocket", "httpupgrade", "hysteria"]
SecurityValues = Literal["none", "reality", "tls"]


class StreamSettings(msgspec.Struct):
    network: NetworkValues
    security: SecurityValues | None = None
    grpcSettings: dict[str, Any] | None = None
    wsSettings: dict[str, Any] | None = None
    hysteriaSettings: dict[str, Any] | None = None


class XrayConfig(msgspec.Struct):
    protocol: str
    tag: str
    settings: dict[str, Any]
    streamSettings: StreamSettings | None = None
