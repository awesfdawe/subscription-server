from typing import Literal, Optional, Dict, Any
from pydantic import BaseModel, Field


class ShadowsocksSettings(BaseModel):
    protocol: Literal["shadowsocks"] = "shadowsocks"

    cipher: str = Field(default="aes-128-gcm")
    password: str

    udp_over_tcp: Optional[bool] = Field(default=None, validation_alias="udp-over-tcp")
    udp_over_tcp_version: Optional[int] = Field(default=None, validation_alias="udp-over-tcp-version")

    plugin: Optional[str] = Field(default=None)
    plugin_opts: Optional[Dict[str, Any]] = Field(default=None, validation_alias="plugin-opts")

    level: Optional[int] = Field(default=None)
    email: Optional[str] = Field(default=None)
