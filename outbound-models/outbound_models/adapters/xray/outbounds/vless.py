from outbound_models.schemas.xray import XrayConfig
from outbound_models.schemas.xray.protocols.vless import VlessXray
from outbound_models.exceptions import OutboundError, MissingParameterError
from outbound_models.models.outbounds.vless import VlessOutbound

from ..transports import grpc, ws
from ..security import tls


def _from_xray(xray: XrayConfig) -> VlessOutbound:
    settings = xray.settings

    match settings:
        case VlessXray():
            pass
        case _:
            raise OutboundError("Wrong settings")

    encryption = settings.encryption
    if encryption == "none":
        encryption = None

    transport = None
    security = None
    stream = xray.stream_settings
    if stream:
        match stream.network:
            case "grpc":
                if stream.grpc_settings:
                    transport = grpc._from_xray(stream.grpc_settings)
            case "websocket":
                if stream.ws_settings:
                    transport = ws._from_xray(stream.ws_settings)

        match stream.security:
            case "reality":
                if stream.reality_settings:
                    security = tls._from_xray(stream.reality_settings)
                else:
                    raise MissingParameterError("Reality settings is missing from xray json")
            case "tls":
                if stream.tls_settings:
                    security = tls._from_xray(stream.tls_settings)

    return VlessOutbound(
        server=settings.address,
        server_port=settings.port,
        uuid=settings.id,
        tag=xray.tag,
        encryption=encryption,
        flow=settings.flow,
        transport=transport,
        security=security,
    )
