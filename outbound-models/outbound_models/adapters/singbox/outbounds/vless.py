import msgspec
from typing import Literal

from outbound_models.models.outbounds.vless import VlessOutbound
from outbound_models.models.security.tls import TlsSecurity
from outbound_models.models.transports.grpc import GrpcTransport
from outbound_models.models.transports.ws import WebsocketTransport
from outbound_models.schemas.singbox.outbounds.vless import VlessSingbox
from outbound_models.schemas.singbox.shared import (
    GrpcTransportSingbox,
    RealityOptionsSingbox,
    TlsOptionsSingbox,
    WebsocketTransportSingbox,
)


def _normalize_flow(flow: str | None) -> str | None:
    if flow == "xtls-rprx-vision-udp443":
        return "xtls-rprx-vision"
    return flow


def _to_singbox(vless: VlessOutbound) -> str:
    outbound = VlessSingbox(
        type="vless",
        tag=vless.tag,
        server=vless.server,
        server_port=vless.server_port,
        uuid=str(vless.uuid),
        flow=_normalize_flow(vless.flow),
        tls=_tls_to_singbox(vless.security),
        transport=_transport_to_singbox(vless.transport),
    )
    return msgspec.json.encode(outbound).decode("utf-8")


def _tls_to_singbox(security: TlsSecurity | None) -> TlsOptionsSingbox | None:
    if security is None:
        return None

    utls: dict[Literal["enabled", "fingerprint"], bool | str] | None = None
    if security.fingerprint:
        utls = {"enabled": True, "fingerprint": security.fingerprint}

    reality = None
    if security.reality:
        reality = RealityOptionsSingbox(
            enabled=True,
            public_key=security.reality.public_key,
            short_id=security.reality.short_id,
        )

    return TlsOptionsSingbox(
        enabled=True,
        server_name=security.server_name,
        insecure=security.insecure,
        alpn=security.alpn,
        utls=utls,
        reality=reality,
    )


def _transport_to_singbox(transport: WebsocketTransport | GrpcTransport | None):
    match transport:
        case WebsocketTransport() as ws:
            return WebsocketTransportSingbox(
                type="ws",
                path=ws.path,
                headers=ws.headers,
                max_early_data=ws.max_early_data,
                early_data_header_name=ws.early_data_header_name,
            )
        case GrpcTransport() as grpc:
            return GrpcTransportSingbox(
                type="grpc",
                service_name=grpc.service_name,
                idle_timeout=grpc.idle_timeout,
                ping_timeout=grpc.ping_timeout,
                permit_without_stream=grpc.permit_without_stream,
            )
        case None:
            return None
