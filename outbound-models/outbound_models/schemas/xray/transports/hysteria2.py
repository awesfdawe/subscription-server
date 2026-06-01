import msgspec

from .base import BaseTransportXray


class MasqueradeOptionsXray(msgspec.Struct):
    insecure: bool | None = None


class Hysteria2TransportXray(BaseTransportXray):
    auth: str
    masquerade: MasqueradeOptionsXray | None = None
