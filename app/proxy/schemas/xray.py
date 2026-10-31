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
    meta: dict[str, Any] | None = None


class Users(msgspec.Struct):
    id: str
    encryption: str | None = "none"
    flow: str | None = None
    packet_encoding: str | None = msgspec.field(default=None, name="packetEncoding")


class Vnext(msgspec.Struct):
    address: str
    port: int
    users: list[Users]


class VlessSettings(msgspec.Struct):
    vnext: list[Vnext]


class HysteriaSettings(msgspec.Struct):
    address: str
    port: int
    version: int | str | None = 2


class TlsSettings(msgspec.Struct, rename="camel"):
    server_name: str | None = None
    fingerprint: str | None = None
    alpn: list[str] | None = None
    allow_insecure: bool | None = None
    pinned_peer_cert_sha256: str | None = None


class RealitySettings(msgspec.Struct, rename="camel"):
    public_key: str
    server_name: str | None = None
    fingerprint: str | None = None
    short_id: str | None = None
    spider_x: str | None = None


class HysteriaStreamSettings(msgspec.Struct):
    auth: str
    version: int | str | None = 2


class GrpcStreamSettings(msgspec.Struct, rename="camel"):
    service_name: str | None = None
    authority: str | None = None


class WsStreamSettings(msgspec.Struct, rename="camel"):
    path: str | None = None
    headers: dict[str, str] | None = None


class XhttpExtra(msgspec.Struct, rename="camel"):
    headers: dict[str, str] | None = None
    sc_max_buffered_posts: str | int | None = None
    sc_max_each_post_bytes: str | int | None = None
    sc_min_posts_interval_ms: str | int | None = None
    sc_stream_up_server_secs: str | int | None = None
    server_max_header_bytes: str | int | None = None
    uplink_chunk_size: str | int | None = None
    uplink_data_key: str | None = None
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
    uplink_data_placement: str | int | None = None
    xmux: dict[str, Any] | None = None


class XhttpStreamSettings(msgspec.Struct):
    host: str | None = None
    path: str | None = None
    mode: Literal["auto", "packet-up", "stream-up", "stream-one"] | None = None
    headers: dict[str, str] | None = None
    extra: XhttpExtra | None = None


class StreamSettings(msgspec.Struct, rename="camel"):
    network: str | None = "tcp"
    security: str | None = "none"
    tls_settings: TlsSettings | None = None
    reality_settings: RealitySettings | None = None
    hysteria_settings: HysteriaStreamSettings | None = None
    grpc_settings: GrpcStreamSettings | None = None
    ws_settings: WsStreamSettings | None = None
    xhttp_settings: XhttpStreamSettings | None = None


class Outbound(msgspec.Struct, rename="camel"):
    tag_: str = msgspec.field(name="tag")
    stream_settings: StreamSettings | None = None


class Vless(Outbound, tag_field="protocol", tag="vless", rename="camel", kw_only=True):
    settings: VlessSettings


class Hysteria(Outbound, tag_field="protocol", tag="hysteria", rename="camel", kw_only=True):
    settings: HysteriaSettings


class Hysteria2(Outbound, tag_field="protocol", tag="hysteria2", rename="camel", kw_only=True):
    settings: HysteriaSettings


XrayOutbounds = Vless | Hysteria | Hysteria2
