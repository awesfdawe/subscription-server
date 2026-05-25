from typing import Literal
from msgspec import Struct

from .base import BaseSecurity


utls_fingerprints = Literal[
    "chrome", "firefox", "safari", "ios", "android", "edge", "360", "qq", "random", "randomized"
]


class EchOptions(Struct):
    config_path: str | None = None
    query_server_name: str | None = None


class RealityOptions(Struct):
    public_key: str | None = None
    short_id: str | None = None


class TlsSecurity(BaseSecurity, tag="tls"):
    server_name: str | None = None
    fingerprint: utls_fingerprints | None = None
    alpn: list[str] | None = None
    insecure: bool | None = None
    ech: EchOptions | None = None
    reality: RealityOptions | None = None
