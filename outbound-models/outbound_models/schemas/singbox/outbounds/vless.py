import msgspec
from typing import Literal

from outbound_models.schemas.singbox.shared import AnyTransportSingbox, TlsOptionsSingbox


class VlessSingbox(msgspec.Struct, kw_only=True, omit_defaults=True):
    type: Literal["vless"]
    tag: str
    server: str
    server_port: int
    uuid: str
    flow: str | None = None
    tls: TlsOptionsSingbox | None = None
    transport: AnyTransportSingbox | None = None
