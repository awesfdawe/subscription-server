from outbound_models.models.security.tls import utls_fingerprints

from .base import BaseSecurityXray


class TlsSecurityXray(BaseSecurityXray, rename="camel", kw_only=True):
    server_name: str | None = None
    alpn: list[str] | None = None
    allow_insecure: bool | None = None
    fingerprint: utls_fingerprints | None = None
