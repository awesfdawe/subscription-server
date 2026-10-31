from typing import cast

import msgspec
from loguru import logger
from msgspec import UNSET

from app.proxy.schemas.mihomo import GrpcOptions as MihomoGrpcOptions
from app.proxy.schemas.mihomo import Hysteria as MihomoHysteria
from app.proxy.schemas.mihomo import MihomoOutbounds
from app.proxy.schemas.mihomo import RealityOptions as MihomoRealityOptions
from app.proxy.schemas.mihomo import ReuseSettings as MihomoReuseSettings
from app.proxy.schemas.mihomo import Vless as MihomoVless
from app.proxy.schemas.mihomo import WsOptions as MihomoWsOptions
from app.proxy.schemas.mihomo import XhttpOptions as MihomoXhttpOptions
from app.proxy.schemas.xray import Hysteria as XrayHysteria
from app.proxy.schemas.xray import Hysteria2 as XrayHysteria2
from app.proxy.schemas.xray import Vless as XrayVless
from app.proxy.schemas.xray import XrayConfigSchema, XrayOutbounds


def _map_vless(outbound: XrayVless) -> MihomoVless:
    flow = UNSET
    user_flow = outbound.settings.vnext[0].users[0].flow
    if user_flow and user_flow.startswith("xtls-rprx-vision"):
        flow = "xtls-rprx-vision"

    tls = UNSET
    servername = UNSET
    alpn = UNSET
    fingerprint = UNSET
    skip_cert_verify = UNSET
    client_fingerprint = UNSET
    reality_options = UNSET
    network = "tcp"
    grpc_opts = UNSET
    ws_opts = UNSET
    xhttp_opts = UNSET
    packet_encoding = "xudp"

    user_pe = outbound.settings.vnext[0].users[0].packet_encoding
    if user_pe:
        user_pe_lower = user_pe.lower()
        if user_pe_lower in ("xudp", "packetaddr"):
            packet_encoding = user_pe_lower
        elif user_pe_lower in ("none", ""):
            packet_encoding = UNSET

    stream_settings = outbound.stream_settings
    if stream_settings:
        if stream_settings.security in ("reality", "tls"):
            tls = True

        tls_settings = stream_settings.tls_settings
        if tls_settings:
            if tls_settings.server_name:
                servername = tls_settings.server_name
            if tls_settings.alpn:
                alpn = tls_settings.alpn
            if tls_settings.allow_insecure:
                skip_cert_verify = True
            if tls_settings.pinned_peer_cert_sha256:
                fingerprint = tls_settings.pinned_peer_cert_sha256
            if tls_settings.fingerprint:
                if len(tls_settings.fingerprint) == 64:
                    fingerprint = tls_settings.fingerprint
                else:
                    client_fingerprint = tls_settings.fingerprint

        reality_settings = stream_settings.reality_settings
        if reality_settings:
            if reality_settings.server_name:
                servername = reality_settings.server_name
            if reality_settings.fingerprint:
                client_fingerprint = reality_settings.fingerprint
            reality_options = MihomoRealityOptions(
                public_key=reality_settings.public_key,
                short_id=reality_settings.short_id or UNSET,
                spider_x=reality_settings.spider_x or UNSET,
            )

        grpc_settings = stream_settings.grpc_settings
        if grpc_settings or stream_settings.network == "grpc":
            network = "grpc"
            grpc_opts = MihomoGrpcOptions(grpc_service_name=(grpc_settings.service_name if grpc_settings else "") or "")

        ws_settings = stream_settings.ws_settings
        if ws_settings or stream_settings.network == "ws":
            network = "ws"
            ws_path = ws_settings.path if ws_settings and ws_settings.path else UNSET
            ws_headers = ws_settings.headers if ws_settings and ws_settings.headers else UNSET
            ws_opts = MihomoWsOptions(path=ws_path, headers=ws_headers)

        xhttp_settings = stream_settings.xhttp_settings
        if xhttp_settings or stream_settings.network in ("xhttp", "splithttp"):
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
            uplink_data_key = UNSET
            uplink_chunk_size = UNSET
            sc_max_each_post_bytes = UNSET
            sc_min_posts_interval_ms = UNSET
            reuse_settings = UNSET

            if xhttp_settings:
                if xhttp_settings.path:
                    path = xhttp_settings.path
                if xhttp_settings.host:
                    host = xhttp_settings.host
                if xhttp_settings.mode:
                    mode = xhttp_settings.mode
                if xhttp_settings.headers:
                    headers = dict(xhttp_settings.headers)

                extra = xhttp_settings.extra
                if extra:
                    if extra.headers:
                        headers = {**(headers or {}), **extra.headers}
                    if extra.no_grpc_header is not None:
                        no_grpc_header = extra.no_grpc_header
                    if extra.x_padding_bytes:
                        x_padding_bytes = extra.x_padding_bytes
                    if extra.x_padding_obfs_mode is not None:
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
                    if extra.uplink_data_placement is not None:
                        uplink_data_placement = extra.uplink_data_placement
                    if extra.uplink_data_key:
                        uplink_data_key = extra.uplink_data_key
                    if extra.uplink_chunk_size is not None:
                        uplink_chunk_size = extra.uplink_chunk_size
                    if extra.sc_max_each_post_bytes is not None:
                        sc_max_each_post_bytes = extra.sc_max_each_post_bytes
                    if extra.sc_min_posts_interval_ms is not None:
                        sc_min_posts_interval_ms = extra.sc_min_posts_interval_ms
                    if extra.xmux:
                        max_concurrency = extra.xmux.get("maxConcurrency") or UNSET
                        max_connections = extra.xmux.get("maxConnections") or UNSET
                        c_max_reuse_times = extra.xmux.get("cMaxReuseTimes")
                        if c_max_reuse_times is None:
                            c_max_reuse_times = UNSET
                        h_max_request_times = extra.xmux.get("hMaxRequestTimes") or UNSET
                        h_max_reusable_secs = extra.xmux.get("hMaxReusableSecs") or UNSET
                        h_keep_alive_period = extra.xmux.get("hKeepAlivePeriod")
                        if h_keep_alive_period is None:
                            h_keep_alive_period = UNSET
                        reuse_settings = MihomoReuseSettings(
                            max_concurrency=max_concurrency,
                            max_connections=max_connections,
                            c_max_reuse_times=c_max_reuse_times,
                            h_max_request_times=h_max_request_times,
                            h_max_reusable_secs=h_max_reusable_secs,
                            h_keep_alive_period=h_keep_alive_period,
                        )

            xhttp_opts = MihomoXhttpOptions(
                path=path,
                host=host,
                mode=mode,
                headers=headers or UNSET,
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
                uplink_data_key=uplink_data_key,
                uplink_chunk_size=uplink_chunk_size,
                sc_max_each_post_bytes=sc_max_each_post_bytes,
                sc_min_posts_interval_ms=sc_min_posts_interval_ms,
                reuse_settings=reuse_settings,
            )

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
        fingerprint=fingerprint,
        skip_cert_verify=skip_cert_verify,
        client_fingerprint=client_fingerprint,
        reality_opts=reality_options,
        packet_encoding=packet_encoding,
        network=network,
        grpc_opts=grpc_opts,
        ws_opts=ws_opts,
        xhttp_opts=xhttp_opts,
    )


def _map_hysteria(outbound: XrayHysteria | XrayHysteria2) -> MihomoHysteria:
    if outbound.stream_settings is None or outbound.stream_settings.hysteria_settings is None:
        raise ValueError("No hysteria settings exists when should")

    sni = UNSET
    alpn = UNSET
    skip_cert_verify = UNSET
    fingerprint = UNSET

    tls_settings = outbound.stream_settings.tls_settings
    if tls_settings:
        if tls_settings.server_name:
            sni = tls_settings.server_name
        if tls_settings.alpn:
            alpn = tls_settings.alpn
        if tls_settings.allow_insecure:
            skip_cert_verify = True
        if tls_settings.pinned_peer_cert_sha256:
            fingerprint = tls_settings.pinned_peer_cert_sha256
        elif tls_settings.fingerprint and len(tls_settings.fingerprint) == 64:
            fingerprint = tls_settings.fingerprint

    return MihomoHysteria(
        type_="hysteria2",
        name=outbound.tag_,
        server=outbound.settings.address,
        port=outbound.settings.port,
        password=outbound.stream_settings.hysteria_settings.auth,
        sni=sni,
        alpn=alpn,
        fingerprint=fingerprint,
        skip_cert_verify=skip_cert_verify,
    )


def map_xray_to_mihomo(outbound: XrayOutbounds) -> MihomoOutbounds:
    match outbound:
        case XrayVless():
            return _map_vless(outbound)
        case XrayHysteria() | XrayHysteria2():
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
