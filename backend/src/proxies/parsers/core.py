from urllib.parse import urlparse, parse_qsl, unquote
from typing import Callable, Dict

from src.proxies.models import Proxies
from src.proxies.parsers.uri import vless


class UriParserManager:
    _parsers: Dict[str, Callable] = {"vless": vless.parse}

    @classmethod
    def parse(cls, uri: str) -> Proxies:
        parsed_url = urlparse(uri)
        scheme = parsed_url.scheme.lower()

        if scheme not in cls._parsers:
            raise ValueError(f"Unsupported protocol: {scheme}")

        name = unquote(parsed_url.fragment) if parsed_url.fragment else f"{scheme}_{parsed_url.hostname}"

        parser_func = cls._parsers[scheme]
        return parser_func(parsed_url, dict(parse_qsl(parsed_url.query)), name)
