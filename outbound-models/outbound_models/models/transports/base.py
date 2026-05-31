from msgspec import Struct


class BaseTransport(Struct, tag_field="type", kw_only=True):
    pass
