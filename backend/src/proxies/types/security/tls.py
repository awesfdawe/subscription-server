from typing import Literal, List, Optional
from pydantic import BaseModel, Field


class EchOpts(BaseModel):
    pq_signature_schemes: Optional[List[str]] = Field(default=None, validation_alias="pq-signature-schemes")
    dynamic_record_sizing_disabled: Optional[bool] = Field(
        default=None, validation_alias="dynamic-record-sizing-disabled"
    )
    config: Optional[str] = Field(default=None, validation_alias="config")
    config_list: Optional[str] = Field(default=None, validation_alias="config-list")


class TlsSettings(BaseModel):
    security: Literal["tls"] = "tls"

    tls: bool = True
    server_name: Optional[str] = Field(default=None, validation_alias="servername")
    skip_cert_verify: Optional[bool] = Field(default=None, validation_alias="skip-cert-verify")
    client_fingerprint: Optional[str] = Field(default="chrome", validation_alias="client-fingerprint")
    alpn: Optional[List[str]] = Field(default=["h2", "http/1.1"], validation_alias="alpn")

    min_version: Optional[str] = Field(default=None, validation_alias="min-version")
    max_version: Optional[str] = Field(default=None, validation_alias="max-version")
    cipher_suites: Optional[str] = Field(default=None, validation_alias="cipher-suites")

    disable_system_root: Optional[bool] = Field(default=None, validation_alias="disable-system-root")
    pinned_peer_cert_sha256: Optional[str] = Field(default=None, validation_alias="pinned-peer-cert-sha256")
    verify_peer_cert_by_name: Optional[str] = Field(default=None, validation_alias="verify-peer-cert-by-name")
    reject_unknown_sni: Optional[bool] = Field(default=None, validation_alias="reject-unknown-sni")

    ech_opts: Optional[EchOpts] = Field(default=None, validation_alias="ech-opts")
