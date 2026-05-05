from pydantic import BaseModel, Field
from typing import Dict, Optional, Literal


class WsOpts(BaseModel):
    path: str = Field(default="/")
    headers: Optional[Dict[str, str]] = Field(default=None)
    host: Optional[str] = Field(default=None)
    heartbeat_period: Optional[int] = Field(default=None, validation_alias="heartbeat-period")
    max_early_data: Optional[int] = Field(default=None, validation_alias="max-early-data")
    early_data_header_name: Optional[str] = Field(default=None, validation_alias="early-data-header-name")


class WsTransport(BaseModel):
    transport: Literal["ws"] = "ws"

    ws_opts: Optional[WsOpts] = Field(default=None, validation_alias="ws-opts")
