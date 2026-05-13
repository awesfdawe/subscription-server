from typing import Literal
from pydantic import BaseModel, Field, AliasChoices


class RealityOpts(BaseModel):
    public_key: str = Field(validation_alias=AliasChoices("public-key", "pbk"))
    short_id: str = Field(default="", validation_alias=AliasChoices("short-id", "sid"))
    spider_x: str | None = Field(default=None, validation_alias="spider-x")

    mldsa65_verify: str | None = Field(default=None, validation_alias="mldsa65-verify")


class RealitySettings(BaseModel):
    security: Literal["reality"] = "reality"

    tls: bool = True
    server_name: str | None = Field(default=None, validation_alias=AliasChoices("servername", "sni"))
    client_fingerprint: str = Field(default="chrome", validation_alias=AliasChoices("client-fingerprint", "fp"))

    alpn: list[str] | None = Field(default=["h2"])

    skip_cert_verify: bool | None = Field(default=None, validation_alias="skip-cert-verify")

    reality_opts: RealityOpts = Field(validation_alias="reality-opts")
