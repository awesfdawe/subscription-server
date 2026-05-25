from .base import BaseTransport


class GrpcTransport(BaseTransport, tag="grpc"):
    service_name: str

    idle_timeout: int | None = None
    ping_timeout: int | None = None
    permit_without_stream: bool | None = None
