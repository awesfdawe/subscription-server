from typing import Self

from .base import BaseTransport


class GrpcTransport(BaseTransport, tag="grpc"):
    service_name: str | None = None

    idle_timeout: int | None = None
    ping_timeout: int | None = None
    permit_without_stream: bool | None = None

    @classmethod
    def from_uri(cls, query: dict[str, list[str]]) -> Self:
        service_name = query.get("serviceName", [None])[0]

        return cls(service_name=service_name)
