import msgspec

from outbound_models.models.outbounds.hysteria2 import GeckoOptions, Hysteria2Outbound, SalamanderOptions


def _format_speed(mbps: int | None) -> str | None:
    if mbps is None:
        return None
    return f"{mbps} Mbps"


def _to_mihomo(hysteria2: Hysteria2Outbound) -> str:
    proxy: dict[str, object] = {
        "name": hysteria2.tag,
        "type": "hysteria2",
        "server": hysteria2.server,
        "port": hysteria2.server_port,
        "password": hysteria2.password,
    }

    if hysteria2.server_ports:
        proxy["ports"] = hysteria2.server_ports

    up = _format_speed(hysteria2.up_mbps)
    if up:
        proxy["up"] = up

    down = _format_speed(hysteria2.down_mbps)
    if down:
        proxy["down"] = down

    match hysteria2.obfuscation:
        case SalamanderOptions() as salamander:
            proxy["obfs"] = "salamander"
            proxy["obfs-password"] = salamander.password
        case GeckoOptions() as gecko:
            proxy["obfs"] = "gecko"
            proxy["obfs-password"] = gecko.password
        case None:
            pass

    if hysteria2.tls:
        if hysteria2.tls.server_name:
            proxy["sni"] = hysteria2.tls.server_name
        if hysteria2.tls.insecure is not None:
            proxy["skip-cert-verify"] = hysteria2.tls.insecure
        if hysteria2.tls.pin_sha256:
            proxy["fingerprint"] = hysteria2.tls.pin_sha256

    return msgspec.yaml.encode(proxy).decode("utf-8")
