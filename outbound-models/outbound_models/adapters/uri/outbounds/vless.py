from typing import get_args, cast
from uuid import UUID
from urllib.parse import SplitResult, urlunsplit, urlencode, quote, unquote

from outbound_models.exceptions import MissingParameterError
from outbound_models.models.outbounds import VlessOutbound
from outbound_models.models.outbounds.vless import FlowValues

from .. import transports
from ..security import tls


def from_uri(parsed: SplitResult, query: dict[str, list[str]]) -> VlessOutbound:
    if not parsed.username:
        raise MissingParameterError("The UUID is missing from the URI")

    raw_encryption = query.get("encryption", [None])[0]

    encryption = None if raw_encryption == "none" else raw_encryption

    raw_flow = query.get("flow", [None])[0]

    flow = cast(FlowValues | None, raw_flow if raw_flow in get_args(FlowValues) else None)

    security = query.get("security", [None])[0]

    match security:
        case "tls" | "reality":
            security = tls.from_uri(query)
        case "none" | _:
            security = None

    transport = query.get("type", [None])[0]

    match transport:
        case "ws":
            transport = transports.ws.from_uri(query)
        case "grpc":
            transport = transports.grpc.from_uri(query)
        case "tcp" | "raw" | _:
            transport = None

    if not parsed.hostname:
        raise MissingParameterError("The hostname is missing from the URI")

    if not parsed.port:
        raise MissingParameterError("The port is missing from the URI")

    if not parsed.username:
        raise MissingParameterError("The UUID is missing from the URI")
    try:
        uuid = UUID(parsed.username)
    except ValueError, TypeError:
        raise MissingParameterError("The URI contains an invalid UUID")

    return VlessOutbound(
        server=parsed.hostname,
        server_port=parsed.port,
        tag=unquote(parsed.fragment),
        uuid=uuid,
        encryption=encryption,
        flow=flow,
        security=security,
        transport=transport,
    )


def to_uri(vless: VlessOutbound) -> str:
    netloc = f"{vless.uuid}@{vless.server}:{vless.server_port}"

    query_params = {}

    if vless.encryption:
        query_params.update({"encryption": vless.encryption})

    if vless.flow:
        query_params.update({"flow": vless.flow})

    if vless.security:
        query_params.update(tls.to_uri(vless.security))

    if vless.transport:
        query_params.update(transports.to_uri(vless.transport))
    else:
        query_params.update({"type": "tcp"})
    query_string = urlencode(query_params)

    return urlunsplit(
        SplitResult(scheme="vless", netloc=netloc, path="", query=query_string, fragment=quote(vless.tag))
    )
