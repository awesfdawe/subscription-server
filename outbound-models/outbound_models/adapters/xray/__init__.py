import msgspec

from outbound_models.models.outbounds import AnyOutbound

from .outbounds import vless, hysteria2
from outbound_models.schemas.xray import XrayConfig


def from_xray(xray_json: str) -> AnyOutbound:
    try:
        xray = msgspec.json.decode(xray_json, type=XrayConfig)
    except msgspec.DecodeError as e:
        raise ValueError(f"xray json could not be decoded: {e}")

    match xray.protocol:
        case "vless":
            return vless._from_xray(xray)
        case "hysteria":
            return hysteria2._from_xray(xray)
        case _:
            raise ValueError("Protocol not supported yet")
