from typing import Any, Literal

import msgspec


class Routing(msgspec.Struct):
    balancers: list[dict[str, Any]] | None = None


class XrayConfigSchema(msgspec.Struct, rename="camel"):
    outbounds: list[dict[str, Any]]
    routing: Routing | None = None
    observatory: dict[str, Any] | None = None
    burst_observatory: dict[str, Any] | None = None
    remarks: str | None = None
    meta: dict[str, str] | None = None


class Users(msgspec.Struct):
    id: str
    encryption: Literal["none"]
    flow: Literal["xtls-rprx-vision", ""] | None = None


class Vnext(msgspec.Struct):
    address: str
    port: int
    users: list[Users]


class VlessSettings(msgspec.Struct):
    vnext: list[Vnext]


class HysteriaSettings(msgspec.Struct):
    version: Literal[2]
    address: str
    port: int


class TlsSettings(msgspec.Struct, rename="camel"):
    server_name: str
    fingerprint: str | None = None
    alpn: list[str] | None = None
    allow_insecure: bool | None = None


class RealitySettings(msgspec.Struct, rename="camel"):
    server_name: str
    short_id: str
    public_key: str
    fingerprint: str
    spider_x: str | None = None


class HysteriaStreamSettings(msgspec.Struct):
    version: Literal[2]
    auth: str


class GrpcStreamSettings(msgspec.Struct, rename="camel"):
    service_name: str
    authority: str | None = None


class XhttpExtra(msgspec.Struct, rename="camel"):
    headers: dict[str, str] | None = None
    sc_max_buffered_posts: int | None = None
    sc_max_each_post_bytes: int | None = None
    sc_min_posts_interval_ms: int | None = None
    uplink_http_method: (
        Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"] | None
    ) = msgspec.field(default=None, name="uplinkHTTPMethod")
    x_padding_header: str | None = None
    x_padding_key: str | None = None
    x_padding_method: str | None = None
    x_padding_obfs_mode: bool | None = None
    x_padding_placement: str | None = None
    seq_key: str | None = None
    session_key: str | None = None
    no_sse_header: bool | None = msgspec.field(default=None, name="noSSEHeader")
    no_grpc_header: bool | None = msgspec.field(default=None, name="noGRPCHeader")
    seq_placement: str | None = None
    x_padding_bytes: str | None = None
    session_placement: str | None = None
    uplink_data_placement: int | None = None


class XhttpStreamSettings(msgspec.Struct):
    host: str | None = None
    path: str | None = None
    mode: Literal["auto", "packet-up", "stream-up", "stream-one"] | None = None
    extra: XhttpExtra | None = None


class StreamSettings(msgspec.Struct, rename="camel"):
    network: Literal["tcp", "hysteria", "xhttp", "grpc"]
    security: Literal["reality", "tls", "none"]
    tls_settings: TlsSettings | None = None
    reality_settings: RealitySettings | None = None
    hysteria_settings: HysteriaStreamSettings | None = None
    grpc_settings: GrpcStreamSettings | None = None
    xhttp_settings: XhttpStreamSettings | None = None


class Outbound(msgspec.Struct, rename="camel"):
    tag_: str = msgspec.field(name="tag")
    stream_settings: StreamSettings | None = None


class Vless(Outbound, tag_field="protocol", tag="vless", rename="camel", kw_only=True):
    settings: VlessSettings


class Hysteria(Outbound, tag_field="protocol", tag="hysteria", rename="camel", kw_only=True):
    settings: HysteriaSettings


XrayOutbounds = Vless | Hysteria
