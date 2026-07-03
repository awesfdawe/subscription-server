import msgspec

from outbound_models.models.outbounds.vless import VlessOutbound
from outbound_models.models.security.tls import TlsSecurity
from outbound_models.models.transports.grpc import GrpcTransport
from outbound_models.models.transports.ws import WebsocketTransport


def _normalize_flow(flow: str | None) -> str | None:
    if flow == "xtls-rprx-vision-udp443":
        return "xtls-rprx-vision"
    return flow


def _to_mihomo(vless: VlessOutbound) -> str:
    proxy: dict[str, object] = {
        "name": vless.tag,
        "type": "vless",
        "server": vless.server,
        "port": vless.server_port,
        "uuid": str(vless.uuid),
        "encryption": vless.encryption or "",
        "network": "tcp",
    }

    flow = _normalize_flow(vless.flow)
    if flow:
        proxy["flow"] = flow

    match vless.security:
        case TlsSecurity() as tls:
            proxy["tls"] = True
            if tls.server_name:
                proxy["servername"] = tls.server_name
            if tls.alpn:
                proxy["alpn"] = tls.alpn
            if tls.fingerprint:
                proxy["client-fingerprint"] = tls.fingerprint
            if tls.insecure is not None:
                proxy["skip-cert-verify"] = tls.insecure
            if tls.reality:
                reality_opts: dict[str, object] = {"public-key": tls.reality.public_key}
                if tls.reality.short_id:
                    reality_opts["short-id"] = tls.reality.short_id
                if tls.reality.spider_x:
                    reality_opts["spider-x"] = tls.reality.spider_x
                proxy["reality-opts"] = reality_opts
        case None:
            pass

    match vless.transport:
        case WebsocketTransport() as ws:
            proxy["network"] = "ws"
            ws_opts: dict[str, object] = {}
            if ws.path:
                ws_opts["path"] = ws.path
            if ws.headers:
                ws_opts["headers"] = ws.headers
            if ws.max_early_data is not None:
                ws_opts["max-early-data"] = ws.max_early_data
            if ws.early_data_header_name:
                ws_opts["early-data-header-name"] = ws.early_data_header_name
            if ws_opts:
                proxy["ws-opts"] = ws_opts
        case GrpcTransport() as grpc:
            proxy["network"] = "grpc"
            grpc_opts: dict[str, object] = {}
            if grpc.service_name:
                grpc_opts["grpc-service-name"] = grpc.service_name
            if grpc.ping_timeout is not None:
                grpc_opts["ping-interval"] = grpc.ping_timeout
            if grpc_opts:
                proxy["grpc-opts"] = grpc_opts
        case None:
            pass

    return msgspec.yaml.encode(proxy).decode("utf-8")
