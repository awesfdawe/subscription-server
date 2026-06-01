import msgspec


class BaseTransport(msgspec.Struct, kw_only=True):
    pass
