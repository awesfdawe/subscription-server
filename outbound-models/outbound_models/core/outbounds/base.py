from msgspec import Struct


class BaseOutbound(Struct, tag_field="type"):
    tag: str = "proxy"
