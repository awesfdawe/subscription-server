from outbound_models.models.transports.grpc import GrpcTransport
from functools import partial
from uuid import UUID

from outbound_models.exceptions import MissingParameterError, InputParsingError, InputValidationError
from outbound_models.models.outbounds.vless import VlessOutbound

from ..schemas import XrayConfig
from ..transports import grpc
from ..utils import _get_param


def _from_xray(xray: XrayConfig) -> VlessOutbound:
    get_settings_param = partial(_get_param, xray.settings)

    server = get_settings_param("address")
    if not server:
        raise MissingParameterError("Server is missing from the xray json")
    server = str(server)

    port = get_settings_param("port")
    if not port:
        raise MissingParameterError("Port is missing from the xray json")
    try:
        port = int(port)
    except ValueError, IndexError:
        raise InputParsingError("Port cannot be parsed")

    uuid = get_settings_param("id")
    if not uuid:
        raise MissingParameterError("UUID is missing from the xray json")
    try:
        uuid = UUID(uuid)
    except ValueError, TypeError:
        raise InputValidationError("Xray json contains an invalid UUID")

    encryption = get_settings_param("encryption")
    if encryption == "none":
        encryption = None

    if xray.streamSettings:
        match xray.streamSettings.network:
            case "grpc":
                if xray.streamSettings.grpcSettings:
                    transport = grpc._from_xray(xray.streamSettings.grpcSettings)
                else:
                    transport = GrpcTransport()

    return VlessOutbound(
        server=server,
        server_port=port,
        uuid=uuid,
        tag=xray.tag,
        encryption=encryption,
        flow=get_settings_param("flow"),
        transport=transport,
    )
