import msgspec


class BaseTransport(msgspec.Struct, tag_field="type", kw_only=True):
    pass
