from outbound_models.models.outbounds.base import ServerPort

from .base import BaseProtocolXray


class Hysteria2Xray(BaseProtocolXray, tag="hysteria", kw_only=True):
    address: str
    port: ServerPort
