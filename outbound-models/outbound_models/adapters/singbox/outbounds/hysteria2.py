import msgspec

from outbound_models.models.outbounds.hysteria2 import GeckoOptions, Hysteria2Outbound, SalamanderOptions, TlsOptions
from outbound_models.schemas.singbox.outbounds.hysteria2 import Hysteria2Singbox
from outbound_models.schemas.singbox.shared import (
    GeckoObfsSingbox,
    SalamanderObfsSingbox,
    TlsOptionsSingbox,
)


def _to_singbox(hysteria2: Hysteria2Outbound) -> str:
    outbound = Hysteria2Singbox(
        type="hysteria2",
        tag=hysteria2.tag,
        server=hysteria2.server,
        server_port=hysteria2.server_port,
        server_ports=[_server_ports_to_singbox(hysteria2.server_ports)] if hysteria2.server_ports else None,
        up_mbps=hysteria2.up_mbps,
        down_mbps=hysteria2.down_mbps,
        obfs=_obfs_to_singbox(hysteria2.obfuscation),
        password=_password_to_singbox(hysteria2),
        tls=_tls_to_singbox(hysteria2.tls),
    )
    return msgspec.json.encode(outbound).decode("utf-8")


def _password_to_singbox(hysteria2: Hysteria2Outbound) -> str:
    if hysteria2.username:
        return f"{hysteria2.username}:{hysteria2.password}"
    return hysteria2.password


def _server_ports_to_singbox(server_ports: str) -> str:
    return server_ports.replace("-", ":", 1)


def _obfs_to_singbox(obfuscation: SalamanderOptions | GeckoOptions | None):
    match obfuscation:
        case SalamanderOptions() as salamander:
            return SalamanderObfsSingbox(type="salamander", password=salamander.password)
        case GeckoOptions() as gecko:
            return GeckoObfsSingbox(
                type="gecko",
                password=gecko.password,
                min_packet_size=gecko.min_packet_size,
                max_packet_size=gecko.max_packet_size,
            )
        case None:
            return None


def _tls_to_singbox(tls: TlsOptions | None) -> TlsOptionsSingbox | None:
    if tls is None:
        return None

    return TlsOptionsSingbox(
        enabled=True,
        server_name=tls.server_name,
        insecure=tls.insecure,
    )
