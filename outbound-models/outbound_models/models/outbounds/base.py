from typing import Annotated
from msgspec import Struct, Meta

ServerPort = Annotated[int, Meta(ge=0, le=65535)]


class BaseOutbound(Struct, tag_field="type", kw_only=True):
    tag: str
    server: str
    server_port: ServerPort
