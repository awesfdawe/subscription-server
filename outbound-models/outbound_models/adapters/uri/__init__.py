from urllib.parse import urlsplit, parse_qs

from outbound_models.outbounds.exceptions import UnsupportedProtocolError, InvalidURIError
from outbound_models.outbounds import AnyOutbound
from outbound_models.outbounds.vless import VlessOutbound
from outbound_models.outbounds.hysteria2 import Hysteria2Outbound


def parse(uri: str) -> AnyOutbound:
    parsed = urlsplit(uri)

    if not parsed.scheme or not parsed.netloc:
        raise InvalidURIError()

    query = parse_qs(parsed.query)

    match parsed.scheme.lower():
        case "vless":
            return VlessOutbound.from_uri(parsed, query)
        case "hysteria2" | "hy2":
            return Hysteria2Outbound.from_uri(parsed, query)
        case _:
            raise UnsupportedProtocolError()
