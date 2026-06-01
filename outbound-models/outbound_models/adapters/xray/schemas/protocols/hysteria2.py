from outbound_models.models.outbounds.base import ServerPort

from .base import BaseProtocol


class Hysteria2Protocol(BaseProtocol, tag="hysteria"):
    address: str
    port: ServerPort
