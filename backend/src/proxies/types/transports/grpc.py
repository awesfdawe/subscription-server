from pydantic import BaseModel, Field
from typing import Optional, Literal


class GrpcOpts(BaseModel):
    grpc_service_name: Optional[str] = Field(default=None, validation_alias="grpc-service-name")
    authority: Optional[str] = Field(default=None)
    multi_mode: Optional[bool] = Field(default=None, validation_alias="multi-mode")
    idle_timeout: Optional[int] = Field(default=None, validation_alias="idle-timeout")
    health_check_timeout: Optional[int] = Field(default=None, validation_alias="health-check-timeout")
    permit_without_stream: Optional[bool] = Field(default=None, validation_alias="permit-without-stream")
    initial_windows_size: Optional[int] = Field(default=None, validation_alias="initial-windows-size")
    user_agent: Optional[str] = Field(default=None, validation_alias="user-agent")


class GrpcTransport(BaseModel):
    network: Literal["grpc"] = "grpc"

    grpc_opts: Optional[GrpcOpts] = Field(default=None, validation_alias="grpc-opts")
