from urllib.parse import SplitResult, unquote
from typing import Annotated, NamedTuple
from msgspec import Struct, Meta

from .exceptions import MissingHostError, MissingPortError, MissingTagError


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
            raise MissingHostError()

        if parsed.port is None:
            raise MissingPortError()

        if not parsed.fragment:
            raise MissingTagError()

        return ParsedBaseData(unquote(parsed.fragment), parsed.hostname, parsed.port)
