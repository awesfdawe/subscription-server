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
from proxy_schemas.schemas.xray.stream_settings import SecurityOptions, StreamSettings


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
            try:
                fingerprint = SingboxUtlsFingerprints(stream.tls_settings.fingerprint.value)
                tls.utls = SingboxUtlsOptions(enabled=True, fingerprint=fingerprint)
            except ValueError:
                pass

    if stream.security == SecurityOptions.reality and stream.reality_settings:
        tls.reality = SingboxRealityOptions(
            enabled=True,
            public_key=stream.reality_settings.public_key,
            short_id=stream.reality_settings.short_id,
        )
        if stream.reality_settings.server_name and not tls.server_name:
            tls.server_name = stream.reality_settings.server_name

        if stream.reality_settings.fingerprint is not None and tls.utls is None:
            try:
                fingerprint = SingboxUtlsFingerprints(stream.reality_settings.fingerprint.value)
                tls.utls = SingboxUtlsOptions(enabled=True, fingerprint=fingerprint)
            except ValueError:
                pass

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
