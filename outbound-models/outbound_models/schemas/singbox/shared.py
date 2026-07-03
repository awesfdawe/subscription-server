import msgspec
from typing import Literal


class RealityOptionsSingbox(msgspec.Struct, kw_only=True, omit_defaults=True):
    enabled: bool
    public_key: str
    short_id: str | None = None


class TlsOptionsSingbox(msgspec.Struct, kw_only=True, omit_defaults=True):
    enabled: bool
    server_name: str | None = None
    insecure: bool | None = None
    alpn: list[str] | None = None
    utls: dict[Literal["enabled", "fingerprint"], bool | str] | None = None
    reality: RealityOptionsSingbox | None = None


class WebsocketTransportSingbox(msgspec.Struct, kw_only=True, omit_defaults=True):
    type: Literal["ws"]
    path: str | None = None
    headers: dict[str, str] | None = None
    max_early_data: int | None = None
    early_data_header_name: str | None = None


class GrpcTransportSingbox(msgspec.Struct, kw_only=True, omit_defaults=True):
    type: Literal["grpc"]
    service_name: str | None = None
    idle_timeout: int | None = None
    ping_timeout: int | None = None
    permit_without_stream: bool | None = None


AnyTransportSingbox = WebsocketTransportSingbox | GrpcTransportSingbox


class SalamanderObfsSingbox(msgspec.Struct, kw_only=True, omit_defaults=True):
    type: Literal["salamander"]
    password: str


class GeckoObfsSingbox(msgspec.Struct, kw_only=True, omit_defaults=True):
    type: Literal["gecko"]
    password: str
    min_packet_size: int | None = None
    max_packet_size: int | None = None


AnyObfsSingbox = SalamanderObfsSingbox | GeckoObfsSingbox
