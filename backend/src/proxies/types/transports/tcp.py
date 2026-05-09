from typing import Literal, Optional
from pydantic import BaseModel, Field


class TcpObfsHeader(BaseModel):
    type: Literal["none", "http"] = "none"


class TcpOpts(BaseModel):
    header: Optional[TcpObfsHeader] = None


class TcpTransport(BaseModel):
    transport: Literal["tcp"] = "tcp"

    tcp_opts: Optional[TcpOpts] = Field(default=None, validation_alias="tcp-opts")
