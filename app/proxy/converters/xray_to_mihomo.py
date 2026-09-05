from msgspec import UNSET

from app.proxy.schemas.mihomo import Hysteria as MihomoHysteria
from app.proxy.schemas.mihomo import MihomoOutbounds
from app.proxy.schemas.mihomo import RealityOptions as MihomoRealityOptions
from app.proxy.schemas.mihomo import Vless as MihomoVless
from app.proxy.schemas.xray import Hysteria as XrayHysteria
from app.proxy.schemas.xray import Vless as XrayVless
from app.proxy.schemas.xray import XrayOutbounds


def _map_vless(outbound: XrayVless) -> MihomoVless:
    flow = UNSET
    if outbound.settings.vnext[0].users[0].flow == "xtls-rprx-vision":
        flow = "xtls-rprx-vision"

    tls = UNSET
    servername = UNSET
    alpn = UNSET
    skip_cert_verify = UNSET
    client_fingerprint = UNSET
    reality_options = UNSET

    stream_settings = outbound.stream_settings
    if stream_settings:
        if stream_settings.security in ("reality", "tls"):
            tls = True

        tls_settings = stream_settings.tls_settings
        if tls_settings:
            servername = tls_settings.server_name
            if tls_settings.alpn:
                alpn = tls_settings.alpn
            if tls_settings.allow_insecure:
                skip_cert_verify = True
            if tls_settings.fingerprint:
                client_fingerprint = "chrome"

        reality_settings = stream_settings.reality_settings
        if reality_settings:
            servername = reality_settings.server_name
            reality_options = MihomoRealityOptions(
                public_key=reality_settings.public_key, short_id=reality_settings.short_id
            )

    return MihomoVless(
        type_="vless",
        name=outbound.tag_,
        server=outbound.settings.vnext[0].address,
        port=outbound.settings.vnext[0].port,
        uuid=outbound.settings.vnext[0].users[0].id,
        flow=flow,
        tls=tls,
        servername=servername,
        alpn=alpn,
        skip_cert_verify=skip_cert_verify,
        client_fingerprint=client_fingerprint,
        reality_opts=reality_options,
    )


def _map_hysteria(outbound: XrayHysteria) -> MihomoHysteria:
    if outbound.stream_settings is None or outbound.stream_settings.hysteria_settings is None:
        raise ValueError("No hysteria settings exists when should")

    sni = UNSET

    tls_settings = outbound.stream_settings.tls_settings
    if tls_settings:
        sni = tls_settings.server_name

    return MihomoHysteria(
        type_="hysteria2",
        name=outbound.tag_,
        server=outbound.settings.address,
        port=outbound.settings.port,
        password=outbound.stream_settings.hysteria_settings.auth,
        sni=sni,
    )


def map_xray_to_mihomo(outbound: XrayOutbounds) -> MihomoOutbounds:
    match outbound:
        case XrayVless():
            return _map_vless(outbound)
        case XrayHysteria():
            return _map_hysteria(outbound)
