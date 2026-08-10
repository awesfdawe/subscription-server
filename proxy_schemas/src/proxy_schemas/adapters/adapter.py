
import msgspec
import msgspec.json
from msgspec.json import Decoder, Encoder

from proxy_schemas.exceptions import (
    ConfigParseError,
    UnsupportedProtocolError,
)
from proxy_schemas.schemas.singbox.outbounds.base import Outbound as SingboxOutbound
from proxy_schemas.schemas.singbox.outbounds.vless import VlessOutbound as SingboxVlessOutbound
from proxy_schemas.schemas.xray.outbounds.base import Outbound as XrayOutbound
from proxy_schemas.schemas.xray.outbounds.types import AnyXrayOutbound
from proxy_schemas.schemas.xray.outbounds.vless import VlessOutbound as XrayVlessOutbound

from .xray.outbounds.vless import singbox_vless_to_xray, xray_vless_to_singbox


class OutboundAdapter:
    def __init__(self, encoder: Encoder | None = None, decoder: Decoder | None = None) -> None:
        self.json_encoder = encoder or Encoder()
        self.json_decoder = decoder or Decoder()

    def get_xray_outbounds(self, config: bytes | str | dict | list) -> list[AnyXrayOutbound]:
        if isinstance(config, dict):
            raw_list = config.get("outbounds", [])
        elif isinstance(config, list):
            raw_list = config
        else:
            raw_bytes = config.encode() if isinstance(config, str) else config
            try:
                decoded = self.json_decoder.decode(raw_bytes)
            except msgspec.DecodeError as e:
                raise ConfigParseError(f"Invalid JSON in Xray config: {e}") from e
            if isinstance(decoded, dict):
                raw_list = decoded.get("outbounds", [])
            elif isinstance(decoded, list):
                raw_list = decoded
            else:
                raise ConfigParseError(
                    f"Expected a JSON object at the root of Xray config, got {type(decoded).__name__}"
                )

        if not isinstance(raw_list, list):
            raise ConfigParseError(f"Expected 'outbounds' to be a list, got {type(raw_list).__name__}")

        outbounds = []
        for item in raw_list:
            try:
                item_bytes = self.json_encoder.encode(item)
                outbounds.append(msgspec.json.decode(item_bytes, type=AnyXrayOutbound))
            except (msgspec.ValidationError, msgspec.DecodeError):
                pass

        return outbounds

    # def get_singbox_outbounds(self, config: bytes | str | dict) -> list[AnySingboxOutbound]:
    #     if isinstance(config, dict):
    #         raw_list = config.get("outbounds", [])
    #     else:
    #         raw_bytes = config.encode() if isinstance(config, str) else config
    #         try:
    #             decoded = self.json_decoder.decode(raw_bytes)
    #         except msgspec.DecodeError as e:
    #             raise ConfigParseError(f"Invalid JSON in Singbox config: {e}") from e
    #         if not isinstance(decoded, dict):
    #             raise ConfigParseError(
    #                 f"Expected a JSON object at the root of Singbox config, got {type(decoded).__name__}"
    #             )
    #         raw_list = decoded.get("outbounds", [])

    #     if not isinstance(raw_list, list):
    #         raise ConfigParseError(f"Expected 'outbounds' to be a list, got {type(raw_list).__name__}")

    #     try:
    #         return msgspec.convert(raw_list, list[AnySingboxOutbound])
    #     except msgspec.ValidationError as e:
    #         raise ConfigValidationError(f"Failed to parse Singbox outbounds: {e}") from e

    def xray_to_singbox(self, data: XrayOutbound) -> SingboxOutbound:
        match data:
            case XrayVlessOutbound() as vless:
                return xray_vless_to_singbox(vless)
            case _:
                raise UnsupportedProtocolError(f"Xray protocol '{type(data).__name__}' is not supported yet")

    def singbox_to_xray(self, data: SingboxOutbound) -> XrayOutbound:
        match data:
            case SingboxVlessOutbound() as vless:
                return singbox_vless_to_xray(vless)
            case _:
                raise UnsupportedProtocolError(f"Singbox outbound type '{type(data).__name__}' is not supported yet")
