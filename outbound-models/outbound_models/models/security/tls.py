import msgspec
from typing import Literal

from .base import BaseSecurity


utls_fingerprints = Literal[
    "chrome", "firefox", "safari", "ios", "android", "edge", "360", "qq", "random", "randomized"
]


class RealityOptions(msgspec.Struct, kw_only=True):
    public_key: str
    short_id: str | None = None
    spider_x: str | None = None


class TlsSecurity(BaseSecurity, tag="tls", kw_only=True):
    server_name: str | None = None
    fingerprint: utls_fingerprints | None = None
    alpn: list[str] | None = None
    insecure: bool | None = None
    reality: RealityOptions | None = None
