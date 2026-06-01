import msgspec


class MasqueradeOptions(msgspec.Struct):
    insecure: bool | None = None


class Hysteria2Transport(msgspec.Struct):
    auth: str
    masquerade: MasqueradeOptions | None = None
