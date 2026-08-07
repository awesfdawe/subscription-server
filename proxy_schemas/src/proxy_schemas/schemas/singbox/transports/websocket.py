from typing import Annotated

from msgspec import Meta

from .base import Transport


class WebsocketTransport(Transport, tag="ws", kw_only=True, forbid_unknown_fields=True):
    headers: dict[str, str] | None = None
    max_early_data: Annotated[int, Meta(ge=0, le=4294967295)] | None = None
    path: str | None = None
    early_data_header_name: str | None = None
