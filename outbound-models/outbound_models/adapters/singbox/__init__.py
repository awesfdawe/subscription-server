from outbound_models.models.outbounds import AnyOutbound, Hysteria2Outbound, VlessOutbound

from .outbounds import hysteria2, vless


def to_singbox(outbound: AnyOutbound) -> str:
    match outbound:
        case VlessOutbound():
            return vless._to_singbox(outbound)
        case Hysteria2Outbound():
            return hysteria2._to_singbox(outbound)
        case _:
            raise ValueError("Protocol not supported yet")
