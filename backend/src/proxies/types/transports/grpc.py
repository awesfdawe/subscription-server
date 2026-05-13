from pydantic import BaseModel, Field
from typing import Literal


class GrpcOpts(BaseModel):
    grpc_service_name: str | None = Field(default=None, validation_alias="grpc-service-name")
    authority: str | None = Field(default=None)
    multi_mode: bool | None = Field(default=None, validation_alias="multi-mode")
    idle_timeout: int | None = Field(default=None, validation_alias="idle-timeout")
    health_check_timeout: int | None = Field(default=None, validation_alias="health-check-timeout")
    permit_without_stream: bool | None = Field(default=None, validation_alias="permit-without-stream")
    initial_windows_size: int | None = Field(default=None, validation_alias="initial-windows-size")
    user_agent: str | None = Field(default=None, validation_alias="user-agent")


class GrpcTransport(BaseModel):
    transport: Literal["grpc"] = "grpc"

    grpc_opts: GrpcOpts | None = Field(default=None, validation_alias="grpc-opts")
