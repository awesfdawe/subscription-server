from functools import partial
from urllib.parse import SplitResult, unquote

from outbound_models.exceptions import MissingParameterError
from outbound_models.models.outbounds.hysteria2 import TlsOptions, Hysteria2Outbound, SalamanderOptions, GeckoOptions

from ..utils import _get_param


def _from_uri(parsed: SplitResult, query: dict[str, list[str]]) -> Hysteria2Outbound:
    get_param = partial(_get_param, query)

    if not parsed.hostname:
        raise MissingParameterError("The hostname is missing from the URI")

    username = None
    if parsed.username and parsed.password:
        username = parsed.username
        password = parsed.password
    elif parsed.username:
        password = parsed.username
    else:
        raise MissingParameterError("No credentials are present in the URI")

    raw_port = parsed.netloc.split("@")[-1].rsplit(":", 1)[1]
    ports_list = raw_port.split(",")
    match len(ports_list):
        case 2:
            server_port = ports_list[0]
            server_ports = ports_list[1]
        case 1:
            server_port = ports_list[0]
            server_ports = None
        case _:
            raise MissingParameterError("Port is missing from the URI")

    server_name = get_param("sni")
    pin_sha256 = get_param("pinSHA256")
    match get_param("insecure"):
        case "1":
            insecure = True
        case "0":
            insecure = False
        case _:
            insecure = None

    tls_params = {"server_name": server_name, "insecure": insecure, "pin_sha256": pin_sha256}
    tls = TlsOptions(**tls_params) if any(tls_params.values()) else None

    obfs_password = get_param("obfs-password")

    obfuscation = None
    if obfs_password is not None:
        match get_param("obfs"):
            case "salamander":
                obfuscation = SalamanderOptions(obfs_password)
            case "gecko":
                obfuscation = GeckoOptions(obfs_password)

    return Hysteria2Outbound(
        server=parsed.hostname,
        server_port=int(server_port),
        server_ports=server_ports,
        tag=unquote(parsed.fragment),
        password=password,
        username=username,
        obfuscation=obfuscation,
        tls=tls,
    )
