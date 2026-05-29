from msgspec import Struct

from .base import BaseTransport


class SalamanderOptions(Struct, tag="salamander"):
    password: str


class GeckoOptions(Struct, tag="gecko"):
    password: str

    min_packet_size: int | None = None
    max_packet_size: int | None = None


ObfuscationOptions = SalamanderOptions | GeckoOptions


class Hysteria2Transport(BaseTransport, tag="hysteria2"):
    password: str

    up_mbps: int | None = None
    down_mbps: int | None = None
    obfuscation: ObfuscationOptions | None = None
