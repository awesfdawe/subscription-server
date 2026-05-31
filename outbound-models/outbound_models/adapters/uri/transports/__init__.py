from outbound_models.models.transports.ws import WebsocketTransport
from outbound_models.models.transports.grpc import GrpcTransport
from outbound_models.models.transports import AnyTransport

from . import grpc, ws


def _to_uri(transport: AnyTransport) -> dict[str, str]:
    match transport:
        case GrpcTransport():
            return grpc._to_uri(transport)
        case WebsocketTransport():
            return ws._to_uri(transport)
