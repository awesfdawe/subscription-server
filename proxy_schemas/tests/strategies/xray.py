from hypothesis import strategies as st
from proxy_schemas.schemas.xray.outbounds.vless import (
    Flows as XrayFlows,
)
from proxy_schemas.schemas.xray.outbounds.vless import (
    VlessOutbound as XrayVlessOutbound,
)
from proxy_schemas.schemas.xray.outbounds.vless import (
    VlessSettings,
    VlessUser,
    VlessVnext,
)
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

tags_st = st.text(
    alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"), whitelist_characters="-_"), min_size=1, max_size=20
)
servers_st = st.text(
    alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"), whitelist_characters=".-"), min_size=3, max_size=30
)
ports_st = st.integers(min_value=1, max_value=65535)
uuids_st = st.uuids().map(str)
xray_flows_st = st.sampled_from(list(XrayFlows))
utls_fp_st = st.sampled_from(list(XrayUtlsFingerprints))


@st.composite
def xray_tls_settings_st(draw):
    return XrayTlsOptions(
        server_name=draw(st.one_of(st.none(), servers_st)),
        allow_insecure=draw(st.one_of(st.none(), st.booleans())),
        alpn=draw(st.one_of(st.none(), st.lists(st.sampled_from(["h2", "http/1.1"]), min_size=1, max_size=2))),
        fingerprint=draw(st.one_of(st.none(), utls_fp_st)),
    )


@st.composite
def xray_reality_settings_st(draw):
    return XrayRealityOptions(
        server_name=draw(servers_st),
        public_key=draw(st.text(min_size=10, max_size=44)),
        short_id=draw(st.text(alphabet="0123456789abcdef", min_size=8, max_size=16)),
        fingerprint=draw(st.one_of(st.none(), utls_fp_st)),
    )


@st.composite
def xray_ws_settings_st(draw):
    return XrayWebsocketTransport(
        path=draw(st.sampled_from(["/", "/ws", "/path"])),
        headers=draw(st.one_of(st.none(), st.builds(dict, Host=servers_st))),
    )


@st.composite
def xray_grpc_settings_st(draw):
    return XrayGrpcTransport(
        service_name=draw(
            st.text(
                alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"), whitelist_characters="-_"),
                min_size=1,
                max_size=20,
            )
        ),
    )


@st.composite
def xray_stream_settings_st(draw):
    sec = draw(st.sampled_from(list(SecurityOptions)))
    tls_set = None
    reality_set = None
    if sec == SecurityOptions.tls:
        tls_set = draw(xray_tls_settings_st())
    elif sec == SecurityOptions.reality:
        reality_set = draw(xray_reality_settings_st())

    trans_choice = draw(st.sampled_from(["raw", "ws", "grpc"]))
    method = None
    ws_set = None
    grpc_set = None

    if trans_choice == "ws":
        method = TransportOptions.websocket
        ws_set = draw(xray_ws_settings_st())
    elif trans_choice == "grpc":
        method = TransportOptions.grpc
        grpc_set = draw(xray_grpc_settings_st())

    return StreamSettings(
        method=method,
        security=sec,
        tls_settings=tls_set,
        reality_settings=reality_set,
        ws_settings=ws_set,
        grpc_settings=grpc_set,
    )


@st.composite
def xray_vless_flat_st(draw):
    return XrayVlessOutbound(
        label=draw(tags_st),
        settings=VlessSettings(
            address=draw(servers_st),
            port=draw(ports_st),
            id=draw(uuids_st),
            encryption="none",
            flow=draw(st.one_of(st.none(), xray_flows_st)),
        ),
        stream_settings=draw(xray_stream_settings_st()),
    )


@st.composite
def xray_vless_legacy_st(draw):
    user = VlessUser(
        id=draw(uuids_st),
        encryption="none",
        flow=draw(st.one_of(st.none(), xray_flows_st)),
    )
    vnext = VlessVnext(
        address=draw(servers_st),
        port=draw(ports_st),
        users=[user],
    )
    return XrayVlessOutbound(
        label=draw(tags_st),
        settings=VlessSettings(
            vnext=[vnext],
        ),
        stream_settings=draw(xray_stream_settings_st()),
    )


def xray_vless_any_st():
    return st.one_of(xray_vless_flat_st(), xray_vless_legacy_st())
