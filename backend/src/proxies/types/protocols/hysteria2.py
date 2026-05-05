from typing import Literal, Optional, List
from pydantic import BaseModel, Field


class Hysteria2Settings(BaseModel):
    protocol: Literal["hysteria2"] = "hysteria2"

    password: str

    up: Optional[str] = Field(default=None)
    down: Optional[str] = Field(default=None)

    obfs: Optional[str] = Field(default=None)
    obfs_password: Optional[str] = Field(default=None, alias="obfs-password")

    sni: Optional[str] = Field(default=None)
    skip_cert_verify: Optional[bool] = Field(default=None, alias="skip-cert-verify")
    alpn: Optional[List[str]] = Field(default=None)
    fingerprint: Optional[str] = Field(default=None)
