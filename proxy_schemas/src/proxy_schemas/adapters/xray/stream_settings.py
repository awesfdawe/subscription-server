import contextlib

from proxy_schemas.schemas.singbox.tls import (
    RealityOptions as SingboxRealityOptions,
)
from proxy_schemas.schemas.singbox.tls import (
    TlsOptions as SingboxTlsOptions,
)
from proxy_schemas.schemas.singbox.tls import (
    UtlsFingerprints as SingboxUtlsFingerprints,
)
from proxy_schemas.schemas.singbox.tls import (
    UtlsOptions as SingboxUtlsOptions,
)
from proxy_schemas.schemas.singbox.transports.grpc import GrpcTransport as SingboxGrpcTransport
from proxy_schemas.schemas.singbox.transports.types import AnyTransport
from proxy_schemas.schemas.singbox.transports.websocket import WebsocketTransport as SingboxWebsocketTransport
from proxy_schemas.schemas.xray.stream_settings import (
    GrpcTransport as XrayGrpcTransport,
)
from proxy_schemas.schemas.xray.stream_settings import (
    RealityOptions as XrayRealityOptions,
)
from proxy_schemas.schemas.xray.stream_settings import (
    SecurityOptions,
    StreamSettings,
    TransportOptions,
)
from proxy_schemas.schemas.xray.stream_settings import (
    TlsOptions as XrayTlsOptions,
)
from proxy_schemas.schemas.xray.stream_settings import (
    UtlsFingerprints as XrayUtlsFingerprints,
)
from proxy_schemas.schemas.xray.stream_settings import (
    WebsocketTransport as XrayWebsocketTransport,
)


def xray_stream_settings_to_singbox_tls(stream: StreamSettings | None) -> SingboxTlsOptions | None:
    if not stream or stream.security in (None, SecurityOptions.none):
        return None

    tls = SingboxTlsOptions(enabled=True)

    if stream.tls_settings:
        tls.server_name = stream.tls_settings.server_name
        tls.insecure = stream.tls_settings.allow_insecure
        tls.alpn = stream.tls_settings.alpn
        tls.min_version = stream.tls_settings.min_version
        tls.max_version = stream.tls_settings.max_version

        if stream.tls_settings.fingerprint is not None:
            with contextlib.suppress(ValueError):
                tls.utls = SingboxUtlsOptions(
                    enabled=True,
                    fingerprint=SingboxUtlsFingerprints(stream.tls_settings.fingerprint.value),
                )

    if stream.security == SecurityOptions.reality and stream.reality_settings:
        tls.reality = SingboxRealityOptions(
            enabled=True,
            public_key=stream.reality_settings.public_key,
            short_id=stream.reality_settings.short_id,
        )
        if stream.reality_settings.server_name and not tls.server_name:
            tls.server_name = stream.reality_settings.server_name

        if stream.reality_settings.fingerprint is not None and tls.utls is None:
            with contextlib.suppress(ValueError):
                tls.utls = SingboxUtlsOptions(
                    enabled=True,
                    fingerprint=SingboxUtlsFingerprints(stream.reality_settings.fingerprint.value),
                )

    return tls


def xray_stream_settings_to_singbox_transport(stream: StreamSettings | None) -> AnyTransport | None:
    if not stream:
        return None

    if stream.ws_settings is not None:
        return SingboxWebsocketTransport(
            path=stream.ws_settings.path,
            headers=stream.ws_settings.headers,
        )

    if stream.grpc_settings is not None:
        return SingboxGrpcTransport(
            service_name=stream.grpc_settings.service_name,
        )

    return None


def singbox_to_xray_stream_settings(
    tls: SingboxTlsOptions | None,
    transport: AnyTransport | None,
) -> StreamSettings:
    security = SecurityOptions.none
    tls_settings: XrayTlsOptions | None = None
    reality_settings: XrayRealityOptions | None = None
    method: TransportOptions | None = None
    ws_settings: XrayWebsocketTransport | None = None
    grpc_settings: XrayGrpcTransport | None = None

    if tls and tls.enabled:
        fingerprint: XrayUtlsFingerprints | None = None
        if tls.utls and tls.utls.enabled:
            with contextlib.suppress(ValueError):
                fingerprint = XrayUtlsFingerprints(tls.utls.fingerprint.value)

        if tls.reality and tls.reality.enabled:
            security = SecurityOptions.reality
            reality_settings = XrayRealityOptions(
                server_name=tls.server_name or "",
                public_key=tls.reality.public_key,
                short_id=tls.reality.short_id,
                fingerprint=fingerprint,
            )
        else:
            security = SecurityOptions.tls
            tls_settings = XrayTlsOptions(
                server_name=tls.server_name,
                allow_insecure=tls.insecure,
                alpn=tls.alpn,
                min_version=tls.min_version,
                max_version=tls.max_version,
                fingerprint=fingerprint,
            )

    if isinstance(transport, SingboxWebsocketTransport):
        method = TransportOptions.websocket
        ws_settings = XrayWebsocketTransport(
            path=transport.path,
            headers=transport.headers,
        )
    elif isinstance(transport, SingboxGrpcTransport):
        method = TransportOptions.grpc
        grpc_settings = XrayGrpcTransport(
            service_name=transport.service_name,
        )

    return StreamSettings(
        method=method,
        security=security,
        tls_settings=tls_settings,
        reality_settings=reality_settings,
        ws_settings=ws_settings,
        grpc_settings=grpc_settings,
    )
