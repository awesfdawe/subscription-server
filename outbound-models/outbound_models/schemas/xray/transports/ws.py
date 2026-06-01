from .base import BaseTransportXray


class WebsocketTransportXray(BaseTransportXray, kw_only=True):
    path: str | None = None
    headers: dict[str, str] | None = None
