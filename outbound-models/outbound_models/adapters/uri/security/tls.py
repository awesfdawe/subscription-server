from functools import partial
from typing import get_args, cast

from outbound_models.exceptions import MissingParameterError
from outbound_models.models.security.tls import RealityOptions, TlsSecurity, utls_fingerprints

from ..utils import _get_param


def _from_uri(query: dict[str, list[str]]) -> TlsSecurity:
    get_param = partial(_get_param, query)

    reality = None
    if get_param("security") == "reality":
        public_key = get_param("pbk")
        if not public_key:
            raise MissingParameterError("Public key is missing from the URI")

        spider_x = get_param("spx")
        reality = RealityOptions(
            public_key=public_key,
            short_id=get_param("sid"),
            spider_x=None if spider_x == "/" else spider_x,
        )

    fingerprint = get_param("fp")
    fingerprint = cast(
        utls_fingerprints | None,
        fingerprint if fingerprint in get_args(utls_fingerprints) else None,
    )

    alpn = get_param("alpn")
    if alpn:
        alpn = alpn.split(",")
    else:
        alpn = None

    insecure = get_param("insecure") or get_param("allowInsecure")
    match insecure:
        case "1":
            insecure = True
        case "0":
            insecure = False
        case _:
            insecure = None

    return TlsSecurity(
        server_name=get_param("sni"),
        fingerprint=fingerprint,
        alpn=alpn,
        insecure=insecure,
        reality=reality,
    )


def _to_uri(tls: TlsSecurity) -> dict[str, str]:
    query_params = {}

    if tls.server_name:
        query_params.update({"sni": tls.server_name})
    if tls.fingerprint:
        query_params.update({"fp": tls.fingerprint})
    if tls.alpn:
        query_params.update({"alpn": ",".join(tls.alpn)})
    if tls.insecure:
        query_params.update({"insecure": str(int(tls.insecure))})
    if tls.reality:
        query_params.update({"security": "reality"})
        query_params.update({"pbk": tls.reality.public_key})

        if tls.reality.short_id:
            query_params.update({"sid": tls.reality.short_id})
        if tls.reality.spider_x:
            query_params.update({"spx": tls.reality.spider_x})
    else:
        query_params.update({"security": "tls"})

    return query_params
