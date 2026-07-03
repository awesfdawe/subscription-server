import msgspec
from typing import Literal
from uuid import UUID

from outbound_models.models.outbounds.vless import MlkemEncryption, FlowValues
from outbound_models.models.outbounds.base import ServerPort

from .base import BaseProtocolXray


class VnextUserXray(msgspec.Struct, kw_only=True):
    id: UUID
    encryption: str
    flow: FlowValues | None = None


class VnextServerXray(msgspec.Struct, kw_only=True):
    address: str
    port: ServerPort
    users: list[VnextUserXray]


class VlessXray(BaseProtocolXray, tag="vless", kw_only=True):
    address: str | None = None
    port: ServerPort | None = None
    id: UUID | None = None
    encryption: str | None = None
    flow: FlowValues | None = None
    vnext: list[VnextServerXray] | None = None
