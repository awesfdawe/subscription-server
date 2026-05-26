from msgspec import Struct


class BaseOutbound(Struct, tag_field="type", kw_only=True):
    tag: str = "proxy"
