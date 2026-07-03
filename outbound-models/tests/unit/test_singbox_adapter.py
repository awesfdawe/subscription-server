from string import ascii_lowercase, digits
from typing import cast

import msgspec
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from outbound_models.adapters.singbox import to_singbox
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
    header_alphabet = ascii_lowercase + digits + "-_/.:"

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
        "type": "vless",
        "tag": outbound.tag,
        "server": outbound.server,
        "server_port": outbound.server_port,
        "uuid": str(outbound.uuid),
    }

    if outbound.flow:
        expected["flow"] = "xtls-rprx-vision" if outbound.flow == "xtls-rprx-vision-udp443" else outbound.flow

    if security:
        tls: dict[str, object] = {"enabled": True}
        if security.server_name:
            tls["server_name"] = security.server_name
        if security.insecure is not None:
            tls["insecure"] = security.insecure
        if security.alpn:
            tls["alpn"] = security.alpn
        if security.fingerprint:
            tls["utls"] = {"enabled": True, "fingerprint": security.fingerprint}
        if security.reality:
            reality: dict[str, object] = {"enabled": True, "public_key": security.reality.public_key}
            if security.reality.short_id:
                reality["short_id"] = security.reality.short_id
            tls["reality"] = reality
        expected["tls"] = tls

    match transport:
        case WebsocketTransport() as ws:
            transport_payload: dict[str, object] = {"type": "ws"}
            if ws.path:
                transport_payload["path"] = ws.path
            if ws.headers:
                transport_payload["headers"] = ws.headers
            if ws.max_early_data is not None:
                transport_payload["max_early_data"] = ws.max_early_data
            if ws.early_data_header_name:
                transport_payload["early_data_header_name"] = ws.early_data_header_name
            expected["transport"] = transport_payload
        case GrpcTransport() as grpc:
            transport_payload = {"type": "grpc"}
            if grpc.service_name:
                transport_payload["service_name"] = grpc.service_name
            if grpc.idle_timeout is not None:
                transport_payload["idle_timeout"] = grpc.idle_timeout
            if grpc.ping_timeout is not None:
                transport_payload["ping_timeout"] = grpc.ping_timeout
            if grpc.permit_without_stream is not None:
                transport_payload["permit_without_stream"] = grpc.permit_without_stream
            expected["transport"] = transport_payload

    return outbound, expected


@given(generated_vless_outbound())
@settings(max_examples=300)
def test_to_singbox_on_generated_vless_outbounds(outbound_and_expected):
    outbound, expected = outbound_and_expected

    singbox_json = to_singbox(outbound)
    decoded = msgspec.json.decode(singbox_json, type=dict[str, object])

    assert decoded == expected


def test_to_singbox_on_unsupported_outbound():
    class UnsupportedOutbound:
        pass

    with pytest.raises(ValueError):
        to_singbox(cast(VlessOutbound | Hysteria2Outbound, UnsupportedOutbound()))


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
        "type": "hysteria2",
        "tag": outbound.tag,
        "server": outbound.server,
        "server_port": outbound.server_port,
        "password": f"{outbound.username}:{outbound.password}" if outbound.username else outbound.password,
    }

    if outbound.server_ports:
        expected["server_ports"] = [outbound.server_ports.replace("-", ":", 1)]
    if outbound.up_mbps is not None:
        expected["up_mbps"] = outbound.up_mbps
    if outbound.down_mbps is not None:
        expected["down_mbps"] = outbound.down_mbps

    match outbound.obfuscation:
        case SalamanderOptions() as salamander:
            expected["obfs"] = {"type": "salamander", "password": salamander.password}
        case GeckoOptions() as gecko:
            obfs: dict[str, object] = {"type": "gecko", "password": gecko.password}
            if gecko.min_packet_size is not None:
                obfs["min_packet_size"] = gecko.min_packet_size
            if gecko.max_packet_size is not None:
                obfs["max_packet_size"] = gecko.max_packet_size
            expected["obfs"] = obfs

    if outbound.tls:
        tls_payload: dict[str, object] = {"enabled": True}
        if outbound.tls.server_name:
            tls_payload["server_name"] = outbound.tls.server_name
        if outbound.tls.insecure is not None:
            tls_payload["insecure"] = outbound.tls.insecure
        expected["tls"] = tls_payload

    return outbound, expected


@given(generated_hysteria2_outbound())
@settings(max_examples=300)
def test_to_singbox_on_generated_hysteria2_outbounds(outbound_and_expected):
    outbound, expected = outbound_and_expected

    singbox_json = to_singbox(outbound)
    decoded = msgspec.json.decode(singbox_json, type=dict[str, object])

    assert decoded == expected
