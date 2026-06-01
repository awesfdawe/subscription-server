import msgspec


class WebsocketTransport(msgspec.Struct):
    path: str | None = None
    headers: dict[str, str] | None = None
