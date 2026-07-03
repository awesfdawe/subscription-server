from outbound_models.models.outbounds import AnyOutbound, Hysteria2Outbound, VlessOutbound

from .outbounds import hysteria2, vless


def to_mihomo(outbound: AnyOutbound) -> str:
    match outbound:
        case VlessOutbound():
            return vless._to_mihomo(outbound)
        case Hysteria2Outbound():
            return hysteria2._to_mihomo(outbound)
        case _:
            raise ValueError("Protocol not supported yet")
