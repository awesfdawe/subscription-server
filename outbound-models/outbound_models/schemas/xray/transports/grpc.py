import msgspec

from .base import BaseTransportXray


class GrpcTransportXray(BaseTransportXray, kw_only=True):
    service_name: str | None = msgspec.field(default=None, name="serviceName")
    idle_timeout: int | None = None
    health_check_timeout: int | None = None
    permit_without_stream: bool | None = None
