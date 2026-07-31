from msgspec import Struct


class Transport(Struct, kw_only=True, forbid_unknown_fields=True):
    pass
