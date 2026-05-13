from typing import Literal
from pydantic import BaseModel, Field


class EchOpts(BaseModel):
    pq_signature_schemes: list[str] | None = Field(default=None, validation_alias="pq-signature-schemes")
    dynamic_record_sizing_disabled: bool | None = Field(
        default=None, validation_alias="dynamic-record-sizing-disabled"
    )
    config: str | None = Field(default=None, validation_alias="config")
    config_list: str | None = Field(default=None, validation_alias="config-list")


class TlsSettings(BaseModel):
    security: Literal["tls"] = "tls"

    tls: bool = True
    server_name: str | None = Field(default=None, validation_alias="servername")
    skip_cert_verify: bool | None = Field(default=None, validation_alias="skip-cert-verify")
    client_fingerprint: str | None = Field(default="chrome", validation_alias="client-fingerprint")
    alpn: list[str] | None = Field(default=["h2", "http/1.1"], validation_alias="alpn")

    min_version: str | None = Field(default=None, validation_alias="min-version")
    max_version: str | None = Field(default=None, validation_alias="max-version")
    cipher_suites: str | None = Field(default=None, validation_alias="cipher-suites")

    disable_system_root: bool | None = Field(default=None, validation_alias="disable-system-root")
    pinned_peer_cert_sha256: str | None = Field(default=None, validation_alias="pinned-peer-cert-sha256")
    verify_peer_cert_by_name: str | None = Field(default=None, validation_alias="verify-peer-cert-by-name")
    reject_unknown_sni: bool | None = Field(default=None, validation_alias="reject-unknown-sni")

    ech_opts: EchOpts | None = Field(default=None, validation_alias="ech-opts")
