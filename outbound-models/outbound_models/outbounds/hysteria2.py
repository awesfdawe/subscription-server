from urllib.parse import SplitResult
from typing import Annotated, Self
from msgspec import Meta, ValidationError, Struct

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

    @classmethod
    def from_uri(cls, query: dict[str, list[str]]) -> Self:
        server_name = query.get("sni", [None])[0]

        insecure = query.get("insecure", [None])[0]

        if insecure is not None:
            match insecure:
                case "1":
                    insecure = True
                case "0":
                    insecure = False
                case _:
                    insecure = None

        pin_sha256 = query.get("pinSHA256", [None])[0]

        return cls(server_name=server_name, insecure=insecure, pin_sha256=pin_sha256)


class Hysteria2Outbound(BaseOutbound, tag="hysteria2"):
    password: str

    server_ports: Annotated[str, Meta(pattern=r"^\d{1,5}-\d{1,5}$")] | None = None
    up_mbps: int | None = None
    down_mbps: int | None = None
    obfuscation: ObfuscationOptions | None = None
    tls: TlsOptions | None = None

    def __post_init__(self):
        if isinstance(self.server_ports, str):
            left, right = map(int, self.server_ports.split("-"))

            if not (0 <= left <= 65535 and 0 <= right <= 65535):
                raise ValidationError("Ports must be in the range of 1 to 65535")
            if left >= right:
                raise ValidationError(f"The left port ({left}) must be less than the right port ({right})")

    @classmethod
    def from_uri(cls, parsed: SplitResult, query: dict[str, list[str]]) -> Self:
        if not parsed.hostname:
            raise ValueError("Hostname is missing from the URI")

        if parsed.username and parsed.password:
            password = f"{parsed.username}:{parsed.password}"
        elif parsed.username:
            password = parsed.username
        else:
            raise ValueError("The password is missing from the URI")

        raw_port = parsed.netloc.split("@")[-1].rsplit(":", 1)[1]
        ports_list = raw_port.split(",")
        if len(ports_list) == 2:
            server_port = ports_list[0]
            server_ports = ports_list[1]
        else:
            server_port = ports_list[0]
            server_ports = None

        tls = TlsOptions.from_uri(query)

        obfs_password = query.get("obfs-password", [None])[0]

        if obfs_password is not None:
            obfuscation = query.get("obfs", [None])[0]

            match obfuscation:
                case "salamander":
                    obfuscation = SalamanderOptions(obfs_password)
                case "gecko":
                    obfuscation = GeckoOptions(obfs_password)
                case _:
                    obfuscation = None
        else:
            obfuscation = None

        return cls(
            server=parsed.hostname,
            server_port=int(server_port),
            server_ports=server_ports,
            tag=parsed.fragment,
            password=password,
            obfuscation=obfuscation,
            tls=tls,
        )
