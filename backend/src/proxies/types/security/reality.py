from typing import Literal, List, Optional
from pydantic import BaseModel, Field


class RealityOpts(BaseModel):
    public_key: str = Field(validation_alias="public-key")
    short_id: str = Field(default="", validation_alias="short-id")
    spider_x: Optional[str] = Field(default=None, validation_alias="spider-x")

    mldsa65_verify: Optional[str] = Field(default=None, validation_alias="mldsa65-verify")


class RealitySettings(BaseModel):
    security: Literal["reality"] = "reality"

    tls: bool = True
    server_name: Optional[str] = Field(default=None, validation_alias="servername")
    client_fingerprint: str = Field(default="chrome", validation_alias="client-fingerprint")

    alpn: Optional[List[str]] = Field(default=["h2"], validation_alias="alpn")

    skip_cert_verify: Optional[bool] = Field(default=None, validation_alias="skip-cert-verify")

    reality_opts: RealityOpts = Field(validation_alias="reality-opts")
