from string import ascii_lowercase, digits
from typing import cast

import msgspec
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from outbound_models.adapters.mihomo import to_mihomo
from outbound_models.models.outbounds.hysteria2 import GeckoOptions, Hysteria2Outbound, SalamanderOptions, TlsOptions
from outbound_models.models.outbounds.vless import VlessOutbound
from outbound_models.models.security.tls import RealityOptions, TlsSecurity
from outbound_models.models.transports.grpc import GrpcTransport
from outbound_models.models.transports.ws import WebsocketTransport

flow_values = ["xtls-rprx-vision", "xtls-rprx-vision-udp443"]
fingerprints = ["chrome", "firefox", "safari", "ios", "android", "edge", "360", "qq", "random", "randomized"]


def _safe_text(alphabet: str, *, min_size: int, max_size: int):
    return st.text(alphabet=alphabet, min_size=min_size, max_size=max_size)


@st.composite
def generated_vless_outbound(draw):
    host_alphabet = ascii_lowercase + digits + "-."
    tag_alphabet = ascii_lowercase + digits + "-_"
    header_alphabet = ascii_lowercase + digits + "-_/."

    security_kind = draw(st.sampled_from(["none", "tls", "reality"]))
    transport_kind = draw(st.sampled_from(["none", "ws", "grpc"]))
    encryption = draw(st.one_of(st.none(), _safe_text(ascii_lowercase + digits + "/.-_+=", min_size=1, max_size=48)))
    flow = draw(st.one_of(st.none(), st.sampled_from(flow_values)))

    security = None
    if security_kind != "none":
        security = TlsSecurity(
            server_name=draw(st.one_of(st.none(), _safe_text(host_alphabet, min_size=4, max_size=32))),
            fingerprint=draw(st.one_of(st.none(), st.sampled_from(fingerprints))),
            alpn=draw(
                st.one_of(
                    st.none(),
                    st.lists(st.sampled_from(["h2", "http/1.1", "h3"]), min_size=1, max_size=3, unique=True),
                )
            ),
            insecure=draw(st.one_of(st.none(), st.booleans())),
            reality=(
                RealityOptions(
                    public_key=draw(_safe_text(ascii_lowercase + digits + "-_", min_size=8, max_size=48)),
                    short_id=draw(st.one_of(st.none(), _safe_text(ascii_lowercase + digits, min_size=1, max_size=16))),
                    spider_x=draw(st.one_of(st.none(), _safe_text(header_alphabet, min_size=1, max_size=24))),
                )
                if security_kind == "reality"
                else None
            ),
        )

    transport = None
    if transport_kind == "ws":
        transport = WebsocketTransport(
            path=draw(st.one_of(st.none(), _safe_text(header_alphabet, min_size=1, max_size=24))),
            headers=draw(
                st.one_of(
                    st.none(),
                    st.dictionaries(
                        _safe_text(ascii_lowercase + digits + "-", min_size=1, max_size=12),
                        _safe_text(header_alphabet, min_size=1, max_size=24),
                        min_size=1,
                        max_size=3,
                    ),
                )
            ),
            max_early_data=draw(st.one_of(st.none(), st.integers(min_value=0, max_value=65535))),
            early_data_header_name=draw(
                st.one_of(st.none(), _safe_text(ascii_lowercase + digits + "-", min_size=1, max_size=24))
            ),
        )
    elif transport_kind == "grpc":
        transport = GrpcTransport(
            service_name=draw(st.one_of(st.none(), _safe_text(header_alphabet, min_size=1, max_size=24))),
            idle_timeout=draw(st.one_of(st.none(), st.integers(min_value=0, max_value=600))),
            ping_timeout=draw(st.one_of(st.none(), st.integers(min_value=0, max_value=600))),
            permit_without_stream=draw(st.one_of(st.none(), st.booleans())),
        )

    outbound = VlessOutbound(
        tag=draw(_safe_text(tag_alphabet, min_size=1, max_size=24)),
        server=draw(_safe_text(host_alphabet, min_size=4, max_size=32)),
        server_port=draw(st.integers(min_value=1, max_value=65535)),
        uuid=draw(st.uuids()),
        encryption=encryption,
        flow=flow,
        security=security,
        transport=transport,
    )

    expected: dict[str, object] = {
        "name": outbound.tag,
        "type": "vless",
        "server": outbound.server,
        "port": outbound.server_port,
        "uuid": str(outbound.uuid),
        "encryption": outbound.encryption or "",
        "network": "tcp",
    }

    if outbound.flow:
        expected["flow"] = "xtls-rprx-vision" if outbound.flow == "xtls-rprx-vision-udp443" else outbound.flow

    if security:
        expected["tls"] = True
        if security.server_name:
            expected["servername"] = security.server_name
        if security.alpn:
            expected["alpn"] = security.alpn
        if security.fingerprint:
            expected["client-fingerprint"] = security.fingerprint
        if security.insecure is not None:
            expected["skip-cert-verify"] = security.insecure
        if security.reality:
            reality_opts: dict[str, object] = {"public-key": security.reality.public_key}
            if security.reality.short_id:
                reality_opts["short-id"] = security.reality.short_id
            if security.reality.spider_x:
                reality_opts["spider-x"] = security.reality.spider_x
            expected["reality-opts"] = reality_opts

    match transport:
        case WebsocketTransport() as ws:
            expected["network"] = "ws"
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
                expected["ws-opts"] = ws_opts
        case GrpcTransport() as grpc:
            expected["network"] = "grpc"
            grpc_opts: dict[str, object] = {}
            if grpc.service_name:
                grpc_opts["grpc-service-name"] = grpc.service_name
            if grpc.ping_timeout is not None:
                grpc_opts["ping-interval"] = grpc.ping_timeout
            if grpc_opts:
                expected["grpc-opts"] = grpc_opts

    return outbound, expected


@given(generated_vless_outbound())
@settings(max_examples=300)
def test_to_mihomo_on_generated_vless_outbounds(outbound_and_expected):
    outbound, expected = outbound_and_expected

    mihomo_yaml = to_mihomo(outbound)
    decoded = msgspec.yaml.decode(mihomo_yaml, type=dict[str, object])

    assert decoded == expected


def test_to_mihomo_on_unsupported_outbound():
    class UnsupportedOutbound:
        pass

    with pytest.raises(ValueError):
        to_mihomo(cast(VlessOutbound | Hysteria2Outbound, UnsupportedOutbound()))


@st.composite
def generated_hysteria2_outbound(draw):
    host_alphabet = ascii_lowercase + digits + "-."
    tag_alphabet = ascii_lowercase + digits + "-_"
    password_alphabet = ascii_lowercase + digits + "-_@"
    pin_alphabet = ascii_lowercase + digits + "/+=-_"
    obfs_kind = draw(st.sampled_from(["none", "salamander", "gecko"]))

    obfuscation = None
    if obfs_kind == "salamander":
        obfuscation = SalamanderOptions(password=draw(_safe_text(password_alphabet, min_size=1, max_size=32)))
    elif obfs_kind == "gecko":
        obfuscation = GeckoOptions(
            password=draw(_safe_text(password_alphabet, min_size=1, max_size=32)),
            min_packet_size=draw(st.one_of(st.none(), st.integers(min_value=1, max_value=1500))),
            max_packet_size=draw(st.one_of(st.none(), st.integers(min_value=1, max_value=1500))),
        )

    tls = draw(
        st.one_of(
            st.none(),
            st.builds(
                TlsOptions,
                server_name=st.one_of(st.none(), _safe_text(host_alphabet, min_size=4, max_size=32)),
                insecure=st.one_of(st.none(), st.booleans()),
                pin_sha256=st.one_of(st.none(), _safe_text(pin_alphabet, min_size=8, max_size=48)),
            ),
        )
    )

    outbound = Hysteria2Outbound(
        tag=draw(_safe_text(tag_alphabet, min_size=1, max_size=24)),
        server=draw(_safe_text(host_alphabet, min_size=4, max_size=32)),
        server_port=draw(st.integers(min_value=1, max_value=65535)),
        password=draw(_safe_text(password_alphabet, min_size=1, max_size=32)),
        username=draw(st.one_of(st.none(), _safe_text(tag_alphabet, min_size=1, max_size=24))),
        server_ports=draw(
            st.one_of(
                st.none(),
                st.builds(
                    lambda start, end: f"{start}-{end}",
                    st.integers(min_value=1, max_value=65534),
                    st.integers(min_value=2, max_value=65535),
                ).filter(lambda value: int(value.split("-")[0]) < int(value.split("-")[1])),
            )
        ),
        up_mbps=draw(st.one_of(st.none(), st.integers(min_value=1, max_value=10000))),
        down_mbps=draw(st.one_of(st.none(), st.integers(min_value=1, max_value=10000))),
        obfuscation=obfuscation,
        tls=tls,
    )

    expected: dict[str, object] = {
        "name": outbound.tag,
        "type": "hysteria2",
        "server": outbound.server,
        "port": outbound.server_port,
        "password": outbound.password,
    }

    if outbound.server_ports:
        expected["ports"] = outbound.server_ports
    if outbound.up_mbps is not None:
        expected["up"] = f"{outbound.up_mbps} Mbps"
    if outbound.down_mbps is not None:
        expected["down"] = f"{outbound.down_mbps} Mbps"

    match outbound.obfuscation:
        case SalamanderOptions() as salamander:
            expected["obfs"] = "salamander"
            expected["obfs-password"] = salamander.password
        case GeckoOptions() as gecko:
            expected["obfs"] = "gecko"
            expected["obfs-password"] = gecko.password

    if outbound.tls:
        if outbound.tls.server_name:
            expected["sni"] = outbound.tls.server_name
        if outbound.tls.insecure is not None:
            expected["skip-cert-verify"] = outbound.tls.insecure
        if outbound.tls.pin_sha256:
            expected["fingerprint"] = outbound.tls.pin_sha256

    return outbound, expected


@given(generated_hysteria2_outbound())
@settings(max_examples=300)
def test_to_mihomo_on_generated_hysteria2_outbounds(outbound_and_expected):
    outbound, expected = outbound_and_expected

    mihomo_yaml = to_mihomo(outbound)
    decoded = msgspec.yaml.decode(mihomo_yaml, type=dict[str, object])

    assert decoded == expected
