from typing import Literal
from uuid import UUID

from outbound_models.models.outbounds.vless import MlkemEncryption, FlowValues
from outbound_models.models.outbounds.base import ServerPort

from .base import BaseProtocolXray


class VlessXray(BaseProtocolXray, tag="vless", kw_only=True):
    address: str
    port: ServerPort
    id: UUID
    encryption: MlkemEncryption | Literal["none"]
    flow: FlowValues | None = None
