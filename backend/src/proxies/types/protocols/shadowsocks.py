from typing import Literal, Any
from pydantic import BaseModel, Field


class ShadowsocksSettings(BaseModel):
    protocol: Literal["shadowsocks", "ss"] = "shadowsocks"

    cipher: str = Field(default="aes-128-gcm")
    password: str

    udp_over_tcp: bool | None = Field(default=None, validation_alias="udp-over-tcp")
    udp_over_tcp_version: int | None = Field(default=None, validation_alias="udp-over-tcp-version")

    plugin: int | None = Field(default=None)
    plugin_opts: dict[str, Any] | None = Field(default=None, validation_alias="plugin-opts")

    level: int | None = Field(default=None)
    email: str | None = Field(default=None)
