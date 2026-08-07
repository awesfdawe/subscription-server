from hypothesis import strategies as st
from proxy_schemas.schemas.singbox.outbounds.vless import (
    Flows as SingboxFlows,
)
from proxy_schemas.schemas.singbox.outbounds.vless import (
    VlessOutbound as SingboxVlessOutbound,
)
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
from proxy_schemas.schemas.singbox.transports.websocket import WebsocketTransport as SingboxWebsocketTransport

tags_st = st.text(
    alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"), whitelist_characters="-_"), min_size=1, max_size=15
)
servers_st = st.text(
    alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"), whitelist_characters=".-"), min_size=3, max_size=20
)
ports_st = st.integers(min_value=1, max_value=65535)
uuids_st = st.uuids().map(str)
singbox_flows_st = st.sampled_from(list(SingboxFlows))

shared_utls_fp_st = st.sampled_from(
    [
        SingboxUtlsFingerprints.chrome,
        SingboxUtlsFingerprints.firefox,
        SingboxUtlsFingerprints.edge,
        SingboxUtlsFingerprints.safari,
        SingboxUtlsFingerprints.field_360,
        SingboxUtlsFingerprints.qq,
        SingboxUtlsFingerprints.ios,
        SingboxUtlsFingerprints.android,
        SingboxUtlsFingerprints.random,
        SingboxUtlsFingerprints.randomized,
    ]
)


@st.composite
def singbox_tls_st(draw):
    sec_type = draw(st.sampled_from(["none", "tls", "reality"]))
    if sec_type == "none":
        return None

    insecure_val = draw(st.sampled_from([None, True])) if sec_type == "tls" else None
    alpn_val = (
        draw(st.one_of(st.none(), st.lists(st.sampled_from(["h2", "http/1.1"]), min_size=1, max_size=2)))
        if sec_type == "tls"
        else None
    )

    tls = SingboxTlsOptions(
        enabled=True,
        server_name=draw(st.one_of(st.none(), servers_st)),
        insecure=insecure_val,
        alpn=alpn_val,
    )

    if draw(st.booleans()):
        tls.utls = SingboxUtlsOptions(enabled=True, fingerprint=draw(shared_utls_fp_st))

    if sec_type == "reality":
        tls.reality = SingboxRealityOptions(
            enabled=True,
            public_key=draw(
                st.text(
                    alphabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=10, max_size=44
                )
            ),
            short_id=draw(st.text(alphabet="0123456789abcdef", min_size=8, max_size=16)),
        )

    return tls


@st.composite
def singbox_transport_st(draw):
    trans_choice = draw(st.sampled_from(["none", "ws", "grpc"]))
    if trans_choice == "ws":
        return SingboxWebsocketTransport(
            path=draw(st.sampled_from(["/", "/ws", "/path"])),
            headers=draw(st.one_of(st.none(), st.builds(dict, Host=servers_st))),
        )
    if trans_choice == "grpc":
        return SingboxGrpcTransport(
            service_name=draw(
                st.text(
                    alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"), whitelist_characters="-_"),
                    min_size=1,
                    max_size=15,
                )
            ),
        )
    return None


@st.composite
def singbox_vless_st(draw):
    return SingboxVlessOutbound(
        tag=draw(tags_st),
        server=draw(servers_st),
        server_port=draw(ports_st),
        uuid=draw(uuids_st),
        flow=draw(st.one_of(st.none(), singbox_flows_st)),
        tls=draw(singbox_tls_st()),
        transport=draw(singbox_transport_st()),
    )
