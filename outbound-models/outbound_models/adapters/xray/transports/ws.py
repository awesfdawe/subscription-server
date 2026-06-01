from outbound_models.models.transports.ws import WebsocketTransport
from outbound_models.schemas.xray.transports.ws import WebsocketTransportXray


def _from_xray(ws: WebsocketTransportXray) -> WebsocketTransport:
    return WebsocketTransport(path=ws.path, headers=ws.headers)
