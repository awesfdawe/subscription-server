from typing import Literal
from pydantic import BaseModel, Field


class TcpObfsHeader(BaseModel):
    type: Literal["none", "http"] = "none"


class TcpOpts(BaseModel):
    header: TcpObfsHeader | None = None


class TcpTransport(BaseModel):
    transport: Literal["tcp"] = "tcp"

    tcp_opts: TcpOpts | None = Field(default=None, validation_alias="tcp-opts")
