from typing import Literal, Optional
from pydantic import BaseModel, Field


class VlessSettings(BaseModel):
    protocol: Literal["vless"] = "vless"

    uuid: str
    flow: Optional[Literal["xtls-rprx-vision", "xtls-rprx-vision-udp443"]] = Field(default=None)
    encryption: str = Field(default="none")
    udp: Optional[bool] = Field(default=True)
    packet_encoding: Optional[Literal["xudp", "packet"]] = Field(default=None, alias="packet-encoding")
    level: Optional[int] = Field(default=None)
    email: Optional[str] = Field(default=None)
