from typing import Any

from msgspec import Struct


class Routing(Struct):
    balancers: list[dict[str, Any]] | None = None


class XraySchema(Struct, rename="camel"):
    outbounds: list[dict[str, Any]]
    routing: Routing | None = None
    observatory: dict[str, Any] | None = None
    burst_observatory: dict[str, Any] | None = None
    remarks: str | None = None
    meta: dict[str, str] | None = None
