from typing import Annotated

from msgspec import Meta

from .base import Transport

Duration = Annotated[str, Meta(pattern="^[-+]?(((\\d+(\\.\\d*)?|\\.\\d+)(ns|us|µs|μs|ms|s|m|h|d))+|0)$")]


class GrpcTransport(Transport, tag="grpc", kw_only=True, forbid_unknown_fields=True):
    service_name: str
    idle_timeout: Duration | None = None
    ping_timeout: Duration | None = None
