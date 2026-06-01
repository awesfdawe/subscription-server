import msgspec


class BaseSecurity(msgspec.Struct, tag_field="type", kw_only=True):
    pass
