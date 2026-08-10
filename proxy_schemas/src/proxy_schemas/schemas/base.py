from msgspec import Struct


class SchemaBase(Struct, kw_only=True):
    pass
