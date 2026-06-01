import msgspec
from typing import Annotated

ServerPort = Annotated[int, msgspec.Meta(ge=0, le=65535)]


class BaseOutbound(msgspec.Struct, kw_only=True):
    tag: str
    server: str
    server_port: ServerPort
