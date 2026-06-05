from functools import partial
from urllib.parse import SplitResult, unquote, urlencode, urlunsplit, quote

from outbound_models.models.outbounds.hysteria2 import TlsOptions, Hysteria2Outbound, SalamanderOptions, GeckoOptions

from ..utils import _get_param


def _from_uri(parsed: SplitResult, query: dict[str, list[str]]) -> Hysteria2Outbound:
    get_param = partial(_get_param, query)

    if not parsed.hostname:
        raise ValueError("The hostname is missing from the URI")

    username = None
    if parsed.username and parsed.password:
        username = parsed.username
        password = parsed.password
    elif parsed.username:
        password = parsed.username
    else:
        raise ValueError("No credentials are present in the URI")

    server_port = None
    server_ports = None

    try:
        raw_port = parsed.netloc.split("@")[-1].rsplit(":", 1)[1]
    except IndexError:
        raise ValueError("Port is missing from the URI")

    port_parts = raw_port.split(",")
    for part in port_parts:
        if "-" in part:
            bounds = part.split("-")
            try:
                start_port = int(bounds[0])
                int(bounds[1])
            except ValueError, IndexError:
                raise ValueError("Invalid port range format")

            if not server_port:
                server_port = start_port
            server_ports = part

        elif part.isdigit():
            server_port = int(part)
        else:
            raise ValueError("Ports cannot be parsed")

    if not server_port:
        raise ValueError("Ports cannot be parsed")

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
                obfuscation = SalamanderOptions(password=obfs_password)
            case "gecko":
                obfuscation = GeckoOptions(password=obfs_password)

    return Hysteria2Outbound(
        server=parsed.hostname,
        server_port=server_port,
        server_ports=server_ports,
        tag=unquote(parsed.fragment),
        password=password,
        username=username,
        obfuscation=obfuscation,
        tls=tls,
    )


def _to_uri(hy2: Hysteria2Outbound) -> str:
    if hy2.username:
        credentials = f"{hy2.username}:{hy2.password}"
    else:
        credentials = hy2.password

    if hy2.server_ports:
        ports = f"{hy2.server_port},{hy2.server_ports}"
    else:
        ports = hy2.server_port

    netloc = f"{credentials}@{hy2.server}:{ports}"

    query_params = {}

    if hy2.obfuscation:
        query_params.update({"obfs-password": hy2.obfuscation.password})
        match hy2.obfuscation:
            case SalamanderOptions():
                query_params.update({"obfs": "salamander"})
            case GeckoOptions():
                query_params.update({"obfs": "gecko"})
    if hy2.tls:
        if hy2.tls.server_name:
            query_params.update({"sni": hy2.tls.server_name})
        if hy2.tls.insecure:
            query_params.update({"insecure": str(int(hy2.tls.insecure))})
        if hy2.tls.pin_sha256:
            query_params.update({"pinSHA256": hy2.tls.pin_sha256})

    query_string = urlencode(query_params)

    return urlunsplit(
        SplitResult(scheme="hysteria2", netloc=netloc, path="", query=query_string, fragment=quote(hy2.tag))
    )
