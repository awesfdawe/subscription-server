from typing import Literal
from pydantic import BaseModel, Field


class VlessSettings(BaseModel):
    protocol: Literal["vless"] = "vless"

    uuid: str
    flow: Literal["xtls-rprx-vision", "xtls-rprx-vision-udp443"] | None = Field(default=None)
    encryption: str = Field(default="none")
    udp: bool = Field(default=True)
    packet_encoding: Literal["xudp", "packet"] | None = Field(default=None, validation_alias="packet-encoding")
    level: int | None = Field(default=None)
    email: str | None = Field(default=None)
