from urllib.parse import SplitResult, unquote
from typing import Annotated, NamedTuple
from msgspec import Struct, Meta


class ParsedBaseData(NamedTuple):
    tag: str
    server: str
    server_port: int


class BaseOutbound(Struct, tag_field="type", kw_only=True):
    tag: str
    server: str
    server_port: Annotated[int, Meta(ge=0, le=65535)]

    @classmethod
    def _base_parse_uri(cls, parsed: SplitResult) -> ParsedBaseData:
        if not parsed.hostname:
            raise ValueError("The hostname is missing from the URI")

        if parsed.port is None:
            raise ValueError("The port is missing from the URI")

        if not parsed.fragment:
            raise ValueError("The tag is missing from the URI")

        return ParsedBaseData(unquote(parsed.fragment), parsed.hostname, parsed.port)
