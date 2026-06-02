from outbound_models.models.outbounds.hysteria2 import Hysteria2Outbound
from urllib.parse import urlsplit, parse_qs

from outbound_models.exceptions import UnsupportedProtocolError
from outbound_models.models.outbounds import AnyOutbound
from outbound_models.models.outbounds.vless import VlessOutbound

from .outbounds import vless, hysteria2


def from_uri(uri: str) -> AnyOutbound:
    parsed = urlsplit(uri)
    query = parse_qs(parsed.query)

    match parsed.scheme.lower():
        case "vless":
            return vless._from_uri(parsed, query)
        case "hysteria2" | "hy2":
            return hysteria2._from_uri(parsed, query)
        case _:
            raise UnsupportedProtocolError()


def to_uri(outbound: AnyOutbound) -> str:
    match outbound:
        case VlessOutbound():
            return vless._to_uri(outbound)
        case Hysteria2Outbound():
            return hysteria2._to_uri(outbound)
        case _:
            raise UnsupportedProtocolError()
