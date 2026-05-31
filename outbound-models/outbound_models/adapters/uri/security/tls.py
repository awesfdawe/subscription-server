from typing import get_args, cast

from outbound_models.exceptions import MissingParameterError
from outbound_models.models.security.tls import RealityOptions, TlsSecurity, utls_fingerprints


def reality_from_uri(query: dict[str, list[str]]) -> RealityOptions:
    public_key = query.get("pbk", [None])[0]

    if not public_key:
        raise MissingParameterError("The public key is missing from the URI")

    short_id = query.get("sid", [None])[0]

    spider_x = query.get("spx", [None])[0]

    if spider_x == "/":
        spider_x = None

    return RealityOptions(public_key=public_key, short_id=short_id, spider_x=spider_x)


def reality_to_uri(reality: RealityOptions) -> dict[str, str]:
    query_params = {}

    query_params.update({"security": "reality"})

    query_params.update({"pbk": reality.public_key})

    if reality.short_id:
        query_params.update({"sid": reality.short_id})

    if reality.spider_x:
        query_params.update({"spx": reality.spider_x})

    return query_params


def from_uri(query: dict[str, list[str]]) -> TlsSecurity:
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
        reality = reality_from_uri(query)
    else:
        reality = None

    return TlsSecurity(server_name=server_name, fingerprint=fingerprint, alpn=alpn, insecure=insecure, reality=reality)


def to_uri(tls: TlsSecurity) -> dict[str, str]:
    query_params = {}

    if tls.server_name:
        query_params.update({"sni": tls.server_name})

    if tls.fingerprint:
        query_params.update({"fp": tls.fingerprint})

    if tls.alpn:
        query_params.update({"alpn": ",".join(tls.alpn)})

    if tls.insecure:
        query_params.update({"insecure": str(bool(int(tls.insecure)))})

    if tls.reality:
        query_params.update(reality_to_uri(tls.reality))
    else:
        query_params.update({"security": "tls"})

    return query_params
