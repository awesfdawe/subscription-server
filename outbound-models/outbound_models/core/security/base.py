from msgspec import Struct


class BaseSecurity(Struct, tag_field="type", kw_only=True):
    pass
