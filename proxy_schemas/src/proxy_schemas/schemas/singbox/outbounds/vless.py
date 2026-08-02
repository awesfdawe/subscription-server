from enum import StrEnum

from ..tls import TlsOptions
from ..transports.types import AnyTransport
from .base import Outbound


class Flows(StrEnum):
    xtls_rprx_vision = "xtls-rprx-vision"


class VlessOutbound(Outbound, tag="vless"):
    uuid: str
    flow: Flows | None = None
    tls: TlsOptions | None = None
    transport: AnyTransport | None = None
