from functools import partial
from typing import get_args, cast
from uuid import UUID
from urllib.parse import SplitResult, urlunsplit, urlencode, quote, unquote

from outbound_models.exceptions import MissingParameterError
from outbound_models.models.outbounds import VlessOutbound
from outbound_models.models.outbounds.vless import FlowValues

from ..utils import _get_param
from .. import transports
from .. import security
from ..security import tls
from ..transports import grpc, ws


def _from_uri(parsed: SplitResult, query: dict[str, list[str]]) -> VlessOutbound:
    get_param = partial(_get_param, query)

    if not parsed.fragment:
        raise MissingParameterError("Tag is missing from the URI")
    if not parsed.hostname:
        raise MissingParameterError("Server is missing from the URI")
    if not parsed.port:
        raise MissingParameterError("Port is missing from the URI")
    if parsed.username:
        try:
            uuid = UUID(parsed.username)
        except ValueError, TypeError:
            raise MissingParameterError("URI contains an invalid UUID")
    else:
        raise MissingParameterError("UUID is missing from the URI")

    encryption = get_param("encryption")
    if encryption == "None":
        encryption = None

    flow = cast(FlowValues | None, flow if (flow := get_param("flow")) in get_args(FlowValues) else None)

    match get_param("security"):
        case "tls" | "reality":
            security = tls._from_uri(query)
        case "none" | _:
            security = None

    match get_param("type"):
        case "ws":
            transport = ws._from_uri(query)
        case "grpc":
            transport = grpc._from_uri(query)
        case "tcp" | "raw" | _:
            transport = None

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


def _to_uri(vless: VlessOutbound) -> str:
    netloc = f"{vless.uuid}@{vless.server}:{vless.server_port}"

    query_params = {}

    if vless.encryption:
        query_params.update({"encryption": vless.encryption})
    if vless.flow:
        query_params.update({"flow": vless.flow})
    if vless.security:
        query_params.update(security._to_uri(vless.security))
    if vless.transport:
        query_params.update(transports._to_uri(vless.transport))
    else:
        query_params.update({"type": "tcp"})

    query_string = urlencode(query_params)

    return urlunsplit(
        SplitResult(scheme="vless", netloc=netloc, path="", query=query_string, fragment=quote(vless.tag))
    )
