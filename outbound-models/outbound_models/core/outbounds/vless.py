from typing import Annotated, Literal
from msgspec import Meta
from uuid import UUID

from .base import BaseOutbound
from ..transports import AnyTransport
from ..security import AnySecurity

mlkem_encryption_pattern = (
    r"^mlkem768x25519plus\."
    r"(?:native|xorpub|random)\."
    r"(?:0rtt|1rtt)\."
    r"100-[1-9]\d*-\d+"
    r"(?:\.\d+-\d+-\d+\.\d+-\d+-\d+)*\."
    r"[A-Za-z0-9+/=_-]+$"
)


class VlessOutbound(BaseOutbound, tag="vless"):
    server: str
    server_port: Annotated[int, Meta(ge=1, le=65535)]
    uuid: UUID

    encryption: Annotated[str, Meta(pattern=mlkem_encryption_pattern)] | None = None
    flow: Literal["xtls-rprx-vision", "xtls-rprx-vision-udp443"] | None = None
    security: AnySecurity | None = None
    transport: AnyTransport | None = None
