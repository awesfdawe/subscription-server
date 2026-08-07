from msgspec.json import Decoder, Encoder

from proxy_schemas.schemas.singbox.outbounds.base import Outbound as SingboxOutbound
from proxy_schemas.schemas.singbox.outbounds.vless import VlessOutbound as SingboxVlessOutbound
from proxy_schemas.schemas.xray.outbounds.base import Outbound as XrayOutbound
from proxy_schemas.schemas.xray.outbounds.vless import VlessOutbound as XrayVlessOutbound

from .xray.outbounds.vless import singbox_vless_to_xray, xray_vless_to_singbox


class OutboundAdapter:
    def __init__(self, encoder: Encoder | None = None, decoder: Decoder | None = None) -> None:
        self.json_encoder = encoder or Encoder()
        self.json_decoder = decoder or Decoder()

    def xray_to_singbox(self, data: XrayOutbound) -> SingboxOutbound:
        match data:
            case XrayVlessOutbound() as vless:
                return xray_vless_to_singbox(vless)
            case _:
                raise NotImplementedError(f"Unsupported Xray outbound type: {type(data)}")

    def singbox_to_xray(self, data: SingboxOutbound) -> XrayOutbound:
        match data:
            case SingboxVlessOutbound() as vless:
                return singbox_vless_to_xray(vless)
            case _:
                raise NotImplementedError(f"Unsupported Singbox outbound type: {type(data)}")
