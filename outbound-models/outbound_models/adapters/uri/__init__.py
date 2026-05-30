from urllib.parse import urlsplit, parse_qs

from outbound_models.outbounds import AnyOutbound
from outbound_models.outbounds.vless import VlessOutbound
from outbound_models.outbounds.hysteria2 import Hysteria2Outbound


def parse(uri: str) -> AnyOutbound:
    parsed = urlsplit(uri)

    if not parsed.scheme or not parsed.netloc or not parsed.query:
        raise ValueError("The string is not a valid URI")

    query = parse_qs(parsed.query)

    match parsed.scheme.lower():
        case "vless":
            return VlessOutbound.from_uri(parsed, query)
        case "hysteria2" | "hy2":
            return Hysteria2Outbound.from_uri(parsed, query)
        case _:
            raise ValueError("The string is not an outbound URI, or the library does not yet support this protocol")
