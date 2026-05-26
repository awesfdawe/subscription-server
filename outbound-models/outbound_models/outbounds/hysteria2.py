from typing import Annotated
from msgspec import Meta, ValidationError

from .base import BaseOutbound
from .security import AnySecurity
from .transports.hysteria2 import Hysteria2Transport


class Hysteria2Outbound(BaseOutbound, tag="hysteria2"):
    server: str
    server_port: Annotated[int, Meta(ge=0, le=65535)] | Annotated[str, Meta(pattern=r"^\d{1,5}:\d{1,5}$")]
    transport: Hysteria2Transport

    security: AnySecurity | None = None

    def __post_init__(self):
        if isinstance(self.server_port, str):
            left, right = map(int, self.server_port.split(":"))

            if not (0 <= left <= 65535 and 0 <= right <= 65535):
                raise ValidationError("Ports must be in the range of 1 to 65535")
            if left >= right:
                raise ValidationError(f"The left port ({left}) must be less than the right port ({right})")
