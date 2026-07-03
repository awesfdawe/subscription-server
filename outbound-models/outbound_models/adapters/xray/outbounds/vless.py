from outbound_models.schemas.xray import XrayConfig
from outbound_models.schemas.xray.protocols.vless import VlessXray
from outbound_models.models.outbounds.vless import VlessOutbound

from ..transports import grpc, ws
from ..security import tls


def _from_xray(xray: XrayConfig) -> VlessOutbound:
    settings = xray.settings

    match settings:
        case VlessXray():
            pass
        case _:
            raise ValueError("Wrong settings")

    address = settings.address
    port = settings.port
    user_id = settings.id
    encryption = settings.encryption
    flow = settings.flow

    if settings.vnext:
        server = settings.vnext[0]
        if not server.users:
            raise ValueError("VLESS users are missing from xray json")

        user = server.users[0]
        address = server.address
        port = server.port
        user_id = user.id
        encryption = user.encryption
        flow = user.flow

    if address is None or port is None or user_id is None or encryption is None:
        raise ValueError("VLESS settings are missing from xray json")

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
                    raise ValueError("Reality settings is missing from xray json")
            case "tls":
                if stream.tls_settings:
                    security = tls._from_xray(stream.tls_settings)

    return VlessOutbound(
        server=address,
        server_port=port,
        uuid=user_id,
        tag=xray.tag,
        encryption=encryption,
        flow=flow,
        transport=transport,
        security=security,
    )
