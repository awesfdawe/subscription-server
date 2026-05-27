from typing import Literal, Self, get_args, cast
from msgspec import Struct

from .base import BaseSecurity


utls_fingerprints = Literal[
    "chrome", "firefox", "safari", "ios", "android", "edge", "360", "qq", "random", "randomized"
]


class RealityOptions(Struct):
    public_key: str
    short_id: str | None = None
    spider_x: str | None = None

    @classmethod
    def from_uri(cls, query: dict[str, list[str]]) -> Self:
        public_key = query.get("pbk", [None])[0]

        if not public_key:
            raise ValueError("The URI contains the reality parameter but lacks a public key")

        short_id = query.get("sid", [None])[0]

        spider_x = query.get("spx", [None])[0]

        if spider_x == "/":
            spider_x = None

        return cls(public_key=public_key, short_id=short_id, spider_x=spider_x)


class TlsSecurity(BaseSecurity, tag="tls"):
    server_name: str | None = None
    fingerprint: utls_fingerprints | None = None
    alpn: list[str] | None = None
    insecure: bool | None = None
    reality: RealityOptions | None = None

    @classmethod
    def from_uri(cls, query: dict[str, list[str]]) -> Self:
        server_name = query.get("sni", [None])[0]

        raw_fingerprint = query.get("fp", [None])[0]

        fingerprint = cast(
            utls_fingerprints | None, raw_fingerprint if raw_fingerprint in get_args(utls_fingerprints) else None
        )

        alpn = query.get("alpn", [None])[0]

        if alpn:
            alpn = alpn.split(",")
        else:
            alpn = None

        insecure = query.get("insecure") or query.get("allowInsecure") or [None]

        insecure = insecure[0]

        if insecure is not None:
            match insecure:
                case "1":
                    insecure = True
                case "0":
                    insecure = False
                case _:
                    insecure = None

        reality = query.get("security", [None])[0]

        if reality == "reality":
            reality = RealityOptions.from_uri(query)
        else:
            reality = None

        return cls(server_name=server_name, fingerprint=fingerprint, alpn=alpn, insecure=insecure, reality=reality)
