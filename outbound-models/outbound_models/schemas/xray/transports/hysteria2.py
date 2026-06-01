import msgspec

from .base import BaseTransportXray


class MasqueradeOptionsXray(msgspec.Struct, kw_only=True):
    insecure: bool | None = None


class Hysteria2TransportXray(BaseTransportXray, kw_only=True):
    auth: str
    masquerade: MasqueradeOptionsXray | None = None
