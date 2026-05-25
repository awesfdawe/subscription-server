from msgspec import Struct


class BaseTransport(Struct, tag_field="type"):
    pass
