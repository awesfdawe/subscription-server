import msgspec
from typing import Literal

from outbound_models.schemas.singbox.shared import AnyObfsSingbox, TlsOptionsSingbox


class Hysteria2Singbox(msgspec.Struct, kw_only=True, omit_defaults=True):
    type: Literal["hysteria2"]
    tag: str
    server: str
    server_port: int
    server_ports: list[str] | None = None
    up_mbps: int | None = None
    down_mbps: int | None = None
    obfs: AnyObfsSingbox | None = None
    password: str
    tls: TlsOptionsSingbox | None = None
