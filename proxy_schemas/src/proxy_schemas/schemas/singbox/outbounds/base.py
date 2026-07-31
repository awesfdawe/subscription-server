from typing import Annotated

from msgspec import Meta, Struct


class Outbound(Struct, kw_only=True, forbid_unknown_fields=True):
    tag: str
    server: str
    server_port: Annotated[int, Meta(ge=0, le=65535)]
