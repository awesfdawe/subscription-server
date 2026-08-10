from enum import StrEnum

from proxy_schemas.schemas.types import TlsVersion

from .base import XrayBase


class TransportOptions(StrEnum):
    raw = "raw"
    tcp = "tcp"
    grpc = "grpc"
    websocket = "websocket"


class SecurityOptions(StrEnum):
    none = "none"
    reality = "reality"
    tls = "tls"


class GrpcTransport(XrayBase):
    service_name: str
    idle_timeout: int | None = None
    health_check_timeout: int | None = None


class WebsocketTransport(XrayBase):
    path: str | None = None
    headers: dict[str, str] | None = None


class UtlsFingerprints(StrEnum):
    chrome = "chrome"
    firefox = "firefox"
    safari = "safari"
    ios = "ios"
    android = "android"
    edge = "edge"
    browser360 = "360"
    qq = "qq"
    random = "random"
    randomized = "randomized"


class RealityOptions(XrayBase):
    server_name: str
    public_key: str
    short_id: str
    fingerprint: UtlsFingerprints | None = None


class CertificateUsageVariants(StrEnum):
    verify = "verify"
    encipherment = "encipherment"


class CertificateObject(XrayBase):
    usage: CertificateUsageVariants | None = None
    certificate: list[str] | None = None
    key: list[str] | None = None


class TlsOptions(XrayBase):
    server_name: str | None = None
    allow_insecure: bool | None = None
    alpn: list[str] | None = None
    min_version: TlsVersion | None = None
    max_version: TlsVersion | None = None
    certificates: list[CertificateObject] | None = None
    fingerprint: UtlsFingerprints | None = None
    pinned_peer_cert_sha_256: str | None = None


class StreamSettings(XrayBase):
    network: TransportOptions | None = None
    method: TransportOptions | None = None
    grpc_settings: GrpcTransport | None = None
    ws_settings: WebsocketTransport | None = None
    security: SecurityOptions | None = None
    reality_settings: RealityOptions | None = None
    tls_settings: TlsOptions | None = None
    ech_config_list: str | None = None
