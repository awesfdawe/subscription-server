from typing import cast

import msgspec
from loguru import logger
from msgspec import UNSET

from app.proxy.schemas.mihomo import GrpcOptions as MihomoGrpcOptions
from app.proxy.schemas.mihomo import Hysteria as MihomoHysteria
from app.proxy.schemas.mihomo import MihomoOutbounds
from app.proxy.schemas.mihomo import RealityOptions as MihomoRealityOptions
from app.proxy.schemas.mihomo import Vless as MihomoVless
from app.proxy.schemas.mihomo import XhttpOptions as MihomoXhttpOptions
from app.proxy.schemas.xray import Hysteria as XrayHysteria
from app.proxy.schemas.xray import Vless as XrayVless
from app.proxy.schemas.xray import XrayConfigSchema, XrayOutbounds


def _map_vless(outbound: XrayVless) -> MihomoVless:
    flow = UNSET
    if outbound.settings.vnext[0].users[0].flow == "xtls-rprx-vision":
        flow = "xtls-rprx-vision"

    tls = UNSET
    servername = UNSET
    alpn = UNSET
    skip_cert_verify = UNSET
    client_fingerprint = UNSET
    reality_options = UNSET
    network = "tcp"
    grpc_opts = UNSET
    xhttp_opts = UNSET

    stream_settings = outbound.stream_settings
    if stream_settings:
        if stream_settings.security in ("reality", "tls"):
            tls = True

        tls_settings = stream_settings.tls_settings
        if tls_settings:
            servername = tls_settings.server_name
            if tls_settings.alpn:
                alpn = tls_settings.alpn
            if tls_settings.allow_insecure:
                skip_cert_verify = True
            if tls_settings.fingerprint:
                client_fingerprint = tls_settings.fingerprint

        reality_settings = stream_settings.reality_settings
        if reality_settings:
            servername = reality_settings.server_name
            client_fingerprint = reality_settings.fingerprint
            reality_options = MihomoRealityOptions(
                public_key=reality_settings.public_key, short_id=reality_settings.short_id or UNSET
            )
        grpc_settings = stream_settings.grpc_settings
        if grpc_settings:
            network = "grpc"
            grpc_opts = MihomoGrpcOptions(grpc_service_name=grpc_settings.service_name or "")
        xhttp_settings = stream_settings.xhttp_settings
        if xhttp_settings:
            network = "xhttp"
            path = UNSET
            host = UNSET
            mode = UNSET
            headers = UNSET
            no_grpc_header = UNSET
            x_padding_bytes = UNSET
            x_padding_obfs_mode = UNSET
            x_padding_key = UNSET
            x_padding_header = UNSET
            x_padding_placement = UNSET
            x_padding_method = UNSET
            uplink_http_method = UNSET
            session_placement = UNSET
            session_key = UNSET
            seq_placement = UNSET
            seq_key = UNSET
            uplink_data_placement = UNSET
            sc_max_each_post_bytes = UNSET
            sc_min_posts_interval_ms = UNSET
            if xhttp_settings.path:
                path = xhttp_settings.path
            if xhttp_settings.host:
                host = xhttp_settings.host
            if xhttp_settings.mode:
                mode = xhttp_settings.mode

            extra = xhttp_settings.extra
            if extra:
                if extra.headers:
                    headers = extra.headers
                if extra.no_grpc_header:
                    no_grpc_header = extra.no_grpc_header
                if extra.x_padding_bytes:
                    x_padding_bytes = extra.x_padding_bytes
                if extra.x_padding_obfs_mode:
                    x_padding_obfs_mode = extra.x_padding_obfs_mode
                if extra.x_padding_key:
                    x_padding_key = extra.x_padding_key
                if extra.x_padding_header:
                    x_padding_header = extra.x_padding_header
                if extra.x_padding_placement:
                    x_padding_placement = extra.x_padding_placement
                if extra.x_padding_method:
                    x_padding_method = extra.x_padding_method
                if extra.uplink_http_method:
                    uplink_http_method = extra.uplink_http_method
                if extra.session_placement:
                    session_placement = extra.session_placement
                if extra.session_key:
                    session_key = extra.session_key
                if extra.seq_placement:
                    seq_placement = extra.seq_placement
                if extra.seq_key:
                    seq_key = extra.seq_key
                if extra.uplink_data_placement:
                    uplink_data_placement = extra.uplink_data_placement
                if extra.sc_max_each_post_bytes:
                    sc_max_each_post_bytes = extra.sc_max_each_post_bytes
                if extra.sc_min_posts_interval_ms:
                    sc_min_posts_interval_ms = extra.sc_min_posts_interval_ms
            xhttp_opts = MihomoXhttpOptions(
                path=path,
                host=host,
                mode=mode,
                headers=headers,
                no_grpc_header=no_grpc_header,
                x_padding_bytes=x_padding_bytes,
                x_padding_obfs_mode=x_padding_obfs_mode,
                x_padding_key=x_padding_key,
                x_padding_header=x_padding_header,
                x_padding_placement=x_padding_placement,
                x_padding_method=x_padding_method,
                uplink_http_method=uplink_http_method,
                session_placement=session_placement,
                session_key=session_key,
                seq_placement=seq_placement,
                seq_key=seq_key,
                uplink_data_placement=uplink_data_placement,
                sc_max_each_post_bytes=sc_max_each_post_bytes,
                sc_min_posts_interval_ms=sc_min_posts_interval_ms,
            )
            # TODO: rewrite this boilerplate shit later

    return MihomoVless(
        type_="vless",
        name=outbound.tag_,
        server=outbound.settings.vnext[0].address,
        port=outbound.settings.vnext[0].port,
        uuid=outbound.settings.vnext[0].users[0].id,
        flow=flow,
        tls=tls,
        servername=servername,
        alpn=alpn,
        skip_cert_verify=skip_cert_verify,
        client_fingerprint=client_fingerprint,
        reality_opts=reality_options,
        network=network,
        grpc_opts=grpc_opts,
        xhttp_opts=xhttp_opts,
    )


def _map_hysteria(outbound: XrayHysteria) -> MihomoHysteria:
    if outbound.stream_settings is None or outbound.stream_settings.hysteria_settings is None:
        raise ValueError("No hysteria settings exists when should")

    sni = UNSET

    tls_settings = outbound.stream_settings.tls_settings
    if tls_settings:
        sni = tls_settings.server_name

    return MihomoHysteria(
        type_="hysteria2",
        name=outbound.tag_,
        server=outbound.settings.address,
        port=outbound.settings.port,
        password=outbound.stream_settings.hysteria_settings.auth,
        sni=sni,
    )


def map_xray_to_mihomo(outbound: XrayOutbounds) -> MihomoOutbounds:
    match outbound:
        case XrayVless():
            return _map_vless(outbound)
        case XrayHysteria():
            return _map_hysteria(outbound)


def extract_outbound_signatures(configuration: XrayConfigSchema) -> list[bytes]:
    signatures: list[bytes] = []
    for raw_outbound in configuration.outbounds:
        try:
            xray_outbound = msgspec.convert(raw_outbound, type=XrayOutbounds)
            mihomo_outbound = map_xray_to_mihomo(xray_outbound)
        except (msgspec.ValidationError, ValueError) as error:
            logger.error(f"Conversion from xray config to mihomo outbound failed: {error}")
            continue

        anonymous_outbound = msgspec.structs.replace(mihomo_outbound, name="")
        signature = msgspec.json.encode(anonymous_outbound)
        if signature not in signatures:
            signatures.append(signature)
    return signatures


def split_single_and_multi_configurations(
    configurations: list[XrayConfigSchema],
) -> tuple[list[XrayConfigSchema], list[XrayConfigSchema]]:
    configurations_signatures = [extract_outbound_signatures(configuration) for configuration in configurations]

    signature_occurrences: dict[bytes, int] = {}
    for signatures in configurations_signatures:
        for signature in signatures:
            signature_occurrences[signature] = signature_occurrences.get(signature, 0) + 1

    half_configurations_count = len(configurations) / 2
    meaningful_signatures = [
        [signature for signature in signatures if signature_occurrences[signature] <= half_configurations_count]
        for signatures in configurations_signatures
    ]

    single_configurations: list[XrayConfigSchema] = []
    multi_proxy_configurations: list[XrayConfigSchema] = []

    for index, (configuration, signatures) in enumerate(zip(configurations, meaningful_signatures, strict=True)):
        other_configurations_contained = 0
        for other_index, other_signatures in enumerate(meaningful_signatures):
            if other_index == index or not other_signatures:
                continue
            if all(signature in signatures for signature in other_signatures):
                other_configurations_contained += 1

        if other_configurations_contained >= 2:
            multi_proxy_configurations.append(configuration)
        else:
            single_configurations.append(configuration)

    return single_configurations, multi_proxy_configurations


def multi_xray_configs_to_mihomo(
    configs: list[list[XrayConfigSchema]] | list[XrayConfigSchema],
) -> list[MihomoOutbounds]:
    if not configs:
        return []

    first_element = configs[0]
    provider_batches: list[list[XrayConfigSchema]]
    if isinstance(first_element, XrayConfigSchema):
        provider_batches = [cast(list[XrayConfigSchema], configs)]
    else:
        provider_batches = cast(list[list[XrayConfigSchema]], configs)

    mihomo_outbounds: list[MihomoOutbounds] = []

    for batch in provider_batches:
        single_configurations, multi_proxy_configurations = split_single_and_multi_configurations(batch)

        seen_signatures: set[bytes] = set()
        provider_single_outbounds: list[MihomoOutbounds] = []
        provider_multi_outbounds: list[MihomoOutbounds] = []

        for configuration in single_configurations:
            primary_outbound = next(
                (outbound for outbound in configuration.outbounds if outbound.get("tag") == "proxy"),
                configuration.outbounds[0] if configuration.outbounds else None,
            )

            for raw_outbound in configuration.outbounds:
                try:
                    xray_outbound = msgspec.convert(raw_outbound, type=XrayOutbounds)
                    mihomo_outbound = map_xray_to_mihomo(xray_outbound)
                except (msgspec.ValidationError, ValueError) as error:
                    logger.error(f"Conversion from xray config to mihomo outbound failed: {error}")
                    continue

                anonymous_outbound = msgspec.structs.replace(mihomo_outbound, name="")
                signature = msgspec.json.encode(anonymous_outbound)
                if signature in seen_signatures:
                    continue
                seen_signatures.add(signature)

                if configuration.remarks:
                    if raw_outbound is not primary_outbound:
                        mihomo_outbound.name = f"{configuration.remarks} - {xray_outbound.tag_}"
                    else:
                        mihomo_outbound.name = configuration.remarks

                provider_single_outbounds.append(mihomo_outbound)

        for configuration in multi_proxy_configurations:
            for raw_outbound in configuration.outbounds:
                try:
                    xray_outbound = msgspec.convert(raw_outbound, type=XrayOutbounds)
                    mihomo_outbound = map_xray_to_mihomo(xray_outbound)
                except (msgspec.ValidationError, ValueError) as error:
                    logger.error(f"Conversion from xray config to mihomo outbound failed: {error}")
                    continue

                anonymous_outbound = msgspec.structs.replace(mihomo_outbound, name="")
                signature = msgspec.json.encode(anonymous_outbound)
                if signature in seen_signatures:
                    continue
                seen_signatures.add(signature)

                if configuration.remarks:
                    mihomo_outbound.name = f"{configuration.remarks} - {xray_outbound.tag_}"

                provider_multi_outbounds.append(mihomo_outbound)

        mihomo_outbounds.extend(provider_single_outbounds)
        mihomo_outbounds.extend(provider_multi_outbounds)

    used_names: set[str] = set()
    for outbound in mihomo_outbounds:
        base_name = outbound.name
        name = base_name
        counter = 2
        while name in used_names:
            name = f"{base_name} {counter}"
            counter += 1
        used_names.add(name)
        outbound.name = name

    return mihomo_outbounds
