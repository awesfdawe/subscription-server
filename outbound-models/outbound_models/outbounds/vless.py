from typing import Annotated, Literal, Self, get_args, cast
from msgspec import Meta
from uuid import UUID
from urllib.parse import SplitResult

from .base import BaseOutbound
from .transports import AnyTransport
from .security import AnySecurity
from .security.tls import TlsSecurity

mlkem_encryption_pattern = (
    r"^mlkem768x25519plus\."
    r"(?:native|xorpub|random)\."
    r"(?:0rtt|1rtt)\."
    r"100-[1-9]\d*-\d+"
    r"(?:\.\d+-\d+-\d+\.\d+-\d+-\d+)*\."
    r"[A-Za-z0-9+/=_-]+$"
)

FlowValues = Literal["xtls-rprx-vision", "xtls-rprx-vision-udp443"]


class VlessOutbound(BaseOutbound, tag="vless"):
    server: str
    server_port: Annotated[int, Meta(ge=1, le=65535)]
    uuid: UUID

    encryption: Annotated[str, Meta(pattern=mlkem_encryption_pattern)] | None = None
    flow: FlowValues | None = None
    security: AnySecurity | None = None
    transport: AnyTransport | None = None

    @classmethod
    def from_uri(cls, parsed: SplitResult, query: dict[str, list[str]]) -> Self:
        try:
            uuid = UUID(parsed.username)
        except ValueError:
            raise ValueError("The URI contains an invalid UUID")

        if not parsed.hostname:
            raise ValueError("The hostname is missing from the URI")

        if not parsed.port:
            raise ValueError("The port is missing from the URI")

        raw_encryption = query.get("encryption", [None])[0]

        encryption = None if raw_encryption == "none" else raw_encryption

        raw_flow = query.get("flow", [None])[0]

        flow = cast(FlowValues | None, raw_flow if raw_flow in get_args(FlowValues) else None)

        security = query.get("security", [None])[0]

        match security:
            case "tls" | "reality":
                security = TlsSecurity.from_uri(query)
            case _ | "none":
                security = None

        return cls(
            server=parsed.hostname,
            server_port=parsed.port,
            uuid=uuid,
            encryption=encryption,
            flow=flow,
        )
