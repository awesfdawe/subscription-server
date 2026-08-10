from enum import StrEnum

from proxy_schemas.schemas.types import Port

from ..base import XrayBase
from .base import Outbound


class Flows(StrEnum):
    xtls_rprx_vision = "xtls-rprx-vision"
    xtls_rprx_vision_udp443 = "xtls-rprx-vision-udp443"


class VlessUser(XrayBase, kw_only=True):
    id: str
    encryption: str = "none"
    flow: str | None = None


class VlessVnext(XrayBase, kw_only=True):
    address: str
    port: Port
    users: list[VlessUser]


class VlessSettings(XrayBase, kw_only=True):
    vnext: list[VlessVnext] | None = None
    address: str | None = None
    port: Port | None = None
    id: str | None = None
    encryption: str = "none"
    flow: str | None = None


class VlessOutbound(Outbound, tag="vless", kw_only=True):
    settings: VlessSettings | None = None
