from typing import Literal

import msgspec
from msgspec import UNSET, UnsetType


class RealityOptions(msgspec.Struct, rename="kebab"):
    public_key: str
    short_id: str | UnsetType = UNSET
    spider_x: str | UnsetType = UNSET
    support_x25519mlkem768: bool | UnsetType = UNSET


class Outbound(msgspec.Struct, rename="kebab"):
    type_: Literal["vless", "hysteria2"] = msgspec.field(name="type")
    name: str
    server: str
    port: int
    udp: bool = True
    tls: bool | UnsetType = UNSET
    servername: str | UnsetType = UNSET
    alpn: list[str] | UnsetType = UNSET
    fingerprint: str | UnsetType = UNSET
    skip_cert_verify: bool | UnsetType = UNSET
    client_fingerprint: str | UnsetType = UNSET
    reality_opts: RealityOptions | UnsetType = UNSET


class GrpcOptions(msgspec.Struct, rename="kebab"):
    grpc_service_name: str


class WsOptions(msgspec.Struct, rename="kebab"):
    path: str | UnsetType = UNSET
    headers: dict[str, str] | UnsetType = UNSET


class ReuseSettings(msgspec.Struct, rename="kebab"):
    max_concurrency: str | int | UnsetType = UNSET
    max_connections: str | int | UnsetType = UNSET
    c_max_reuse_times: str | int | UnsetType = UNSET
    h_max_request_times: str | int | UnsetType = UNSET
    h_max_reusable_secs: str | int | UnsetType = UNSET
    h_keep_alive_period: int | UnsetType = UNSET


class XhttpOptions(msgspec.Struct, rename="kebab"):
    path: str | UnsetType = UNSET
    host: str | UnsetType = UNSET
    mode: Literal["auto", "packet-up", "stream-up", "stream-one"] | UnsetType = UNSET
    headers: dict[str, str] | UnsetType = UNSET
    no_grpc_header: bool | UnsetType = UNSET
    x_padding_bytes: str | UnsetType = UNSET
    x_padding_obfs_mode: bool | UnsetType = UNSET
    x_padding_key: str | UnsetType = UNSET
    x_padding_header: str | UnsetType = UNSET
    x_padding_placement: str | UnsetType = UNSET
    x_padding_method: str | UnsetType = UNSET
    uplink_http_method: (
        Literal["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE", "PATCH"] | UnsetType
    ) = UNSET
    session_placement: str | UnsetType = UNSET
    session_key: str | UnsetType = UNSET
    seq_placement: str | UnsetType = UNSET
    seq_key: str | UnsetType = UNSET
    uplink_data_placement: str | int | UnsetType = UNSET
    uplink_data_key: str | UnsetType = UNSET
    uplink_chunk_size: str | int | UnsetType = UNSET
    sc_max_each_post_bytes: str | int | UnsetType = UNSET
    sc_min_posts_interval_ms: str | int | UnsetType = UNSET
    reuse_settings: ReuseSettings | UnsetType = UNSET


class Vless(Outbound, rename="kebab", kw_only=True):
    uuid: str
    flow: Literal["xtls-rprx-vision"] | UnsetType = UNSET
    packet_encoding: Literal["xudp", "packetaddr"] | UnsetType = "xudp"
    network: Literal["tcp", "grpc", "xhttp", "ws"] = "tcp"
    grpc_opts: GrpcOptions | UnsetType = UNSET
    ws_opts: WsOptions | UnsetType = UNSET
    xhttp_opts: XhttpOptions | UnsetType = UNSET


class Hysteria(Outbound, rename="kebab", kw_only=True):
    sni: str | UnsetType = UNSET
    ports: str | UnsetType = UNSET
    hop_interval: int | UnsetType = UNSET
    password: str


MihomoOutbounds = Vless | Hysteria
