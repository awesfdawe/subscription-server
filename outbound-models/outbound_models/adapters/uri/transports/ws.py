from outbound_models.models.transports.ws import WebsocketTransport

from ..utils import _get_param


def _from_uri(query: dict[str, list[str]]) -> WebsocketTransport:
    return WebsocketTransport(path=_get_param(query, "path"))


def _to_uri(ws: WebsocketTransport) -> dict[str, str]:
    query_params = {}

    if ws.path:
        query_params.update({"path": ws.path})

    return query_params
