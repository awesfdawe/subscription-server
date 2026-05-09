from typing import Literal, List, Optional
from pydantic import BaseModel, Field, AliasChoices


class RealityOpts(BaseModel):
    public_key: str = Field(validation_alias=AliasChoices("public-key", "pbk"))
    short_id: str = Field(default="", validation_alias=AliasChoices("short-id", "sid"))
    spider_x: Optional[str] = Field(default=None, validation_alias="spider-x")

    mldsa65_verify: Optional[str] = Field(default=None, validation_alias="mldsa65-verify")


class RealitySettings(BaseModel):
    security: Literal["reality"] = "reality"

    tls: bool = True
    server_name: Optional[str] = Field(default=None, validation_alias=AliasChoices("servername", "sni"))
    client_fingerprint: str = Field(default="chrome", validation_alias=AliasChoices("client-fingerprint", "fp"))

    alpn: Optional[List[str]] = Field(default=["h2"])

    skip_cert_verify: Optional[bool] = Field(default=None, validation_alias="skip-cert-verify")

    reality_opts: RealityOpts = Field(validation_alias="reality-opts")
