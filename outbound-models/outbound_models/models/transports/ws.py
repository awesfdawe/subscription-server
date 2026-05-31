from .base import BaseTransport


class WebsocketTransport(BaseTransport, tag="websocket"):
    path: str | None = None
    headers: dict[str, str] | None = None
    max_early_data: int | None = None
    early_data_header_name: str | None = None
