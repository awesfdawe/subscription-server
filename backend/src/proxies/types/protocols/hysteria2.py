from typing import Literal
from pydantic import BaseModel, Field


class Hysteria2Settings(BaseModel):
    protocol: Literal["hysteria2", "hy2"] = "hysteria2"

    password: str

    up: str | None = Field(default=None)
    down: str | None = Field(default=None)

    obfs: str | None = Field(default=None)
    obfs_password: str | None = Field(default=None, validation_alias="obfs-password")

    server_name: str | None = Field(default=None, validation_alias="sni")
    skip_cert_verify: bool | None = Field(default=None, validation_alias="skip-cert-verify")
    alpn: list[str] | None = Field(default=None)
    fingerprint: str | None = Field(default=None)
