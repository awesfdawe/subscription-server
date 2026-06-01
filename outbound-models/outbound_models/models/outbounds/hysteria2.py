import msgspec
from typing import Annotated

from .base import BaseOutbound


class SalamanderOptions(msgspec.Struct, tag="salamander", kw_only=True):
    password: str


class GeckoOptions(msgspec.Struct, tag="gecko", kw_only=True):
    password: str

    min_packet_size: int | None = None
    max_packet_size: int | None = None


ObfuscationOptions = SalamanderOptions | GeckoOptions


class TlsOptions(msgspec.Struct, kw_only=True):
    server_name: str | None = None
    insecure: bool | None = None
    pin_sha256: str | None = None


class Hysteria2Outbound(BaseOutbound, tag="hysteria2", kw_only=True):
    password: str

    username: str | None = None
    server_ports: Annotated[str, msgspec.Meta(pattern=r"^\d{1,5}-\d{1,5}$")] | None = None
    up_mbps: int | None = None
    down_mbps: int | None = None
    obfuscation: ObfuscationOptions | None = None
    tls: TlsOptions | None = None
