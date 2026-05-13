from pydantic import BaseModel, Field
from typing import Literal


class WsOpts(BaseModel):
    path: str = Field(default="/")
    headers: dict[str, str] | None = Field(default=None)
    host: str | None = Field(default=None)
    heartbeat_period: int | None = Field(default=None, validation_alias="heartbeat-period")
    max_early_data: int | None = Field(default=None, validation_alias="max-early-data")
    early_data_header_name: str | None = Field(default=None, validation_alias="early-data-header-name")


class WsTransport(BaseModel):
    transport: Literal["ws"] = "ws"

    ws_opts: WsOpts | None = Field(default=None, validation_alias="ws-opts")
