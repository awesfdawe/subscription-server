from outbound_models.models.security.tls import TlsSecurity, RealityOptions
from outbound_models.schemas.xray.security.reality import RealitySecurityXray
from outbound_models.schemas.xray.security.tls import TlsSecurityXray


def _from_xray(tls: RealitySecurityXray | TlsSecurityXray) -> TlsSecurity:
    reality = None
    match tls:
        case RealitySecurityXray():
            reality = RealityOptions(public_key=tls.public_key, short_id=tls.short_id, spider_x=tls.spider_x)

    return TlsSecurity(
        server_name=tls.server_name,
        fingerprint=tls.fingerprint,
        alpn=tls.alpn,
        insecure=tls.allow_insecure,
        reality=reality,
    )
