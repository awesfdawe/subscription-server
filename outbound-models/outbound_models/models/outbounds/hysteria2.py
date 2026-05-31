from typing import Annotated
from msgspec import Meta, Struct

from .base import BaseOutbound


class SalamanderOptions(Struct, tag="salamander"):
    password: str


class GeckoOptions(Struct, tag="gecko"):
    password: str

    min_packet_size: int | None = None
    max_packet_size: int | None = None


ObfuscationOptions = SalamanderOptions | GeckoOptions


class TlsOptions(Struct):
    server_name: str | None = None
    insecure: bool | None = None
    pin_sha256: str | None = None


class Hysteria2Outbound(BaseOutbound, tag="hysteria2"):
    password: str

    server_ports: Annotated[str, Meta(pattern=r"^\d{1,5}-\d{1,5}$")] | None = None
    up_mbps: int | None = None
    down_mbps: int | None = None
    obfuscation: ObfuscationOptions | None = None
    tls: TlsOptions | None = None
