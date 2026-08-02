from msgspec import Struct


class SchemaBase(Struct, kw_only=True, forbid_unknown_fields=True):
    pass
