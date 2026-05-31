from outbound_models.models.transports.ws import WebsocketTransport


def from_uri(query: dict[str, list[str]]) -> WebsocketTransport:
    path = query.get("path", [None])[0]

    return WebsocketTransport(path=path)


def to_uri(ws: WebsocketTransport) -> dict[str, str]:
    query_params = {}

    if ws.path:
        query_params.update({"path": ws.path})

    return query_params
