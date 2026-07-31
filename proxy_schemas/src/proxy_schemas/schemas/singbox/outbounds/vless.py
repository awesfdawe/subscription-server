from enum import StrEnum

from proxy_schemas.schemas.singbox.security.tls import TlsOptions
from proxy_schemas.schemas.singbox.transports.types import AnyTransport

from .base import Outbound


class Flows(StrEnum):
    xtls_rprx_vision = "xtls-rprx-vision"


class VlessOutbound(Outbound, tag="vless"):
    uuid: str
    flow: Flows | None = None
    tls: TlsOptions | None = None
    transport: AnyTransport | None = None
