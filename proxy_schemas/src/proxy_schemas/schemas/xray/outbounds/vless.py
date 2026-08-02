from enum import StrEnum

from proxy_schemas.schemas.types import Port

from ..base import XrayBase
from .base import Outbound


class Flows(StrEnum):
    xtls_rprx_vision = "xtls-rprx-vision"
    xtls_rprx_vision_udp443 = "xtls-rprx-vision-udp443"


class VlessUser(XrayBase):
    id: str
    encryption: str
    flow: Flows | None = None


class VlessVnext(XrayBase):
    address: str
    port: Port
    users: list[VlessUser]


class LegacyVlessSettings(XrayBase):
    vnext: list[VlessVnext]


class FlatVlessSettings(XrayBase):
    address: str
    port: Port
    id: str
    encryption: str
    flow: Flows | None = None


VlessSettings = LegacyVlessSettings | FlatVlessSettings


class VlessOutbound(Outbound, tag="vless"):
    settings: VlessSettings
