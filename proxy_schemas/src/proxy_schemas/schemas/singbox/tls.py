from enum import StrEnum

from proxy_schemas.schemas.base import SchemaBase
from proxy_schemas.schemas.types import TlsVersion


class CurvePreferences(StrEnum):
    P256 = "P256"
    P384 = "P384"
    P521 = "P521"
    X25519 = "X25519"
    X25519MLKEM768 = "X25519MLKEM768"


class EchOptions(SchemaBase):
    enabled: bool
    config: list[str] | None = None
    query_server_name: str | None = None


class UtlsFingerprints(StrEnum):
    chrome_psk = "chrome_psk"
    chrome_psk_shuffle = "chrome_psk_shuffle"
    chrome_padding_psk_shuffle = "chrome_padding_psk_shuffle"
    chrome_pq = "chrome_pq"
    chrome_pq_psk = "chrome_pq_psk"
    chrome = "chrome"
    firefox = "firefox"
    edge = "edge"
    safari = "safari"
    field_360 = "360"
    qq = "qq"
    ios = "ios"
    android = "android"
    random = "random"
    randomized = "randomized"


class UtlsOptions(SchemaBase):
    enabled: bool
    fingerprint: UtlsFingerprints = UtlsFingerprints.chrome


class RealityOptions(SchemaBase):
    public_key: str
    short_id: str
    enabled: bool


class TlsOptions(SchemaBase):
    enabled: bool
    server_name: str | None = None
    insecure: bool | None = None
    alpn: list[str] | None = None
    min_version: TlsVersion | None = None
    max_version: TlsVersion | None = None
    cipher_suites: list[str] | None = None
    curve_preferences: list[CurvePreferences] | None = None
    certificate: list[str] | None = None
    certificate_public_key_sha256: str | list[str] | None = None
    ech: EchOptions | None = None
    utls: UtlsOptions | None = None
    reality: RealityOptions | None = None
