from .tls import TlsSecurityXray


class RealitySecurityXray(TlsSecurityXray, rename="camel"):
    public_key: str
    short_id: str | None = None
    spider_x: str | None = None
