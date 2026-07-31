from enum import StrEnum

from msgspec import Struct


class TlsVersion(StrEnum):
    V1_0 = "1.0"
    V1_1 = "1.1"
    V1_2 = "1.2"
    V1_3 = "1.3"


class CurvePreferences(StrEnum):
    P256 = "P256"
    P384 = "P384"
    P521 = "P521"
    X25519 = "X25519"
    X25519MLKEM768 = "X25519MLKEM768"


class EchOptions(Struct, kw_only=True, forbid_unknown_fields=True):
    enabled: bool = False
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


class UtlsOptions(Struct, kw_only=True, forbid_unknown_fields=True):
    enabled: bool = False
    fingerprint: UtlsFingerprints = UtlsFingerprints.chrome


class RealityOptions(Struct, kw_only=True, forbid_unknown_fields=True):
    enabled: bool = False
    public_key: str
    short_id: str


class TlsOptions(Struct, kw_only=True, forbid_unknown_fields=True):
    enabled: bool = True
    server_name: str | None = None
    insecure: bool = False
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
