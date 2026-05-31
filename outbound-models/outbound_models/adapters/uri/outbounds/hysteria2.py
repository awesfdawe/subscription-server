from urllib.parse import SplitResult, unquote

from outbound_models.exceptions import MissingParameterError
from outbound_models.models.outbounds.hysteria2 import TlsOptions, Hysteria2Outbound, SalamanderOptions, GeckoOptions


def tls_from_uri(query: dict[str, list[str]]) -> TlsOptions:
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

    return TlsOptions(server_name=server_name, insecure=insecure, pin_sha256=pin_sha256)


def from_uri(parsed: SplitResult, query: dict[str, list[str]]) -> Hysteria2Outbound:
    if not parsed.hostname:
        raise MissingParameterError("The hostname is missing from the URI")

    if parsed.username and parsed.password:
        password = f"{parsed.username}:{parsed.password}"
    elif parsed.username:
        password = parsed.username
    else:
        raise MissingParameterError("No credentials are present in the URI")

    raw_port = parsed.netloc.split("@")[-1].rsplit(":", 1)[1]
    ports_list = raw_port.split(",")
    if len(ports_list) == 2:
        server_port = ports_list[0]
        server_ports = ports_list[1]
    else:
        server_port = ports_list[0]
        server_ports = None

    tls = tls_from_uri(query)

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

    return Hysteria2Outbound(
        server=parsed.hostname,
        server_port=int(server_port),
        server_ports=server_ports,
        tag=unquote(parsed.fragment),
        password=password,
        obfuscation=obfuscation,
        tls=tls,
    )
