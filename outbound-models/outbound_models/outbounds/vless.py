from typing import Annotated, Literal, Self, get_args, cast
from msgspec import Meta
from uuid import UUID
from urllib.parse import SplitResult, urlunsplit, urlencode, quote

from .base import BaseOutbound
from .exceptions import MissingCredentialsError
from .transports import AnyTransport
from .security import AnySecurity
from .security.tls import TlsSecurity
from .transports.ws import WebsocketTransport
from .transports.grpc import GrpcTransport

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
    uuid: UUID

    encryption: Annotated[str, Meta(pattern=mlkem_encryption_pattern)] | None = None
    flow: FlowValues | None = None
    security: AnySecurity | None = None
    transport: AnyTransport | None = None

    @classmethod
    def from_uri(cls, parsed: SplitResult, query: dict[str, list[str]]) -> Self:
        if not parsed.username:
            raise MissingCredentialsError("The UUID is missing from the URI")
        try:
            uuid = UUID(parsed.username)
        except ValueError, TypeError:
            raise MissingCredentialsError("The URI contains an invalid UUID")

        raw_encryption = query.get("encryption", [None])[0]

        encryption = None if raw_encryption == "none" else raw_encryption

        raw_flow = query.get("flow", [None])[0]

        flow = cast(FlowValues | None, raw_flow if raw_flow in get_args(FlowValues) else None)

        security = query.get("security", [None])[0]

        match security:
            case "tls" | "reality":
                security = TlsSecurity.from_uri(query)
            case "none" | _:
                security = None

        transport = query.get("type", [None])[0]

        match transport:
            case "ws":
                transport = WebsocketTransport.from_uri(query)
            case "grpc":
                transport = GrpcTransport.from_uri(query)
            case "tcp" | "raw" | _:
                transport = None

        base_data = cls._base_parse_uri(parsed)
        return cls(
            server=base_data.server,
            server_port=base_data.server_port,
            tag=base_data.tag,
            uuid=uuid,
            encryption=encryption,
            flow=flow,
            security=security,
            transport=transport,
        )

    def to_uri(self) -> str:
        netloc = f"{self.uuid}@{self.server}:{self.server_port}"

        query_params = {}

        if self.encryption:
            query_params.update({"encryption": self.encryption})

        if self.flow:
            query_params.update({"flow": self.flow})

        if self.security:
            query_params.update(self.security.to_uri())

        if self.transport:
            query_params.update(self.transport.to_uri())
        else:
            query_params.update({"type": "tcp"})
        query_string = urlencode(query_params)

        return urlunsplit(
            SplitResult(scheme="vless", netloc=netloc, path="", query=query_string, fragment=quote(self.tag))
        )
