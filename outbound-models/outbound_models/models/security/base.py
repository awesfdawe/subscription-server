import msgspec


class BaseSecurity(msgspec.Struct, kw_only=True):
    pass
