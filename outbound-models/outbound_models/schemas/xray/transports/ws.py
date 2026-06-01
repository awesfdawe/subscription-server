from .base import BaseTransportXray


class WebsocketTransportXray(BaseTransportXray):
    path: str | None = None
    headers: dict[str, str] | None = None
