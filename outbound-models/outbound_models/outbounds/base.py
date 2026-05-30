from urllib.parse import SplitResult, unquote
from typing import Annotated, NamedTuple
from msgspec import Struct, Meta

from .exceptions import MissingHostnameError, MissingPortError, MissingTagError


class ParsedBaseData(NamedTuple):
    tag: str
    server: str
    server_port: int


ServerPort = Annotated[int, Meta(ge=0, le=65535)]


class BaseOutbound(Struct, tag_field="type", kw_only=True):
    tag: str
    server: str
    server_port: ServerPort

    @classmethod
    def _base_parse_uri(cls, parsed: SplitResult) -> ParsedBaseData:
        if not parsed.hostname:
            raise MissingHostnameError("The hostname is missing from the URI")

        if parsed.port is None:
            raise MissingPortError("The port is missing from the URI")

        if not parsed.fragment:
            raise MissingTagError("The tag is missing from the URI")

        return ParsedBaseData(unquote(parsed.fragment), parsed.hostname, parsed.port)
