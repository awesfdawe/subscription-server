import json
from string import ascii_lowercase, digits

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from outbound_models.adapters.xray import from_xray
from outbound_models.models.outbounds.hysteria2 import Hysteria2Outbound, TlsOptions
from outbound_models.models.outbounds.vless import VlessOutbound

flow_values = ["xtls-rprx-vision", "xtls-rprx-vision-udp443"]


def _safe_text(alphabet: str, *, min_size: int, max_size: int):
    return st.text(alphabet=alphabet, min_size=min_size, max_size=max_size)


@st.composite
def valid_xray_vless_payload(draw):
    host_alphabet = ascii_lowercase + digits + "-."
    tag_alphabet = ascii_lowercase + digits + "-_"

    flat_server = draw(_safe_text(host_alphabet, min_size=4, max_size=32))
    flat_port = draw(st.integers(min_value=1, max_value=65535))
    vnext_server = draw(_safe_text(host_alphabet, min_size=4, max_size=32))
    vnext_port = draw(st.integers(min_value=1, max_value=65535))
    tag = draw(_safe_text(tag_alphabet, min_size=1, max_size=24))
    flat_user_id = draw(st.uuids())
    vnext_user_id = draw(st.uuids())
    flat_flow = draw(st.one_of(st.none(), st.sampled_from(flow_values)))
    vnext_flow = draw(st.one_of(st.none(), st.sampled_from(flow_values)))
    mode = draw(st.sampled_from(["flattened", "vnext", "both"]))

    settings_payload: dict[str, object] = {"protocol": "vless"}

    if mode in {"flattened", "both"}:
        settings_payload.update(
            {
                "address": flat_server,
                "port": flat_port,
                "id": str(flat_user_id),
                "encryption": "none",
            }
        )
        if flat_flow is not None:
            settings_payload["flow"] = flat_flow

    if mode in {"vnext", "both"}:
        user_payload: dict[str, object] = {"id": str(vnext_user_id), "encryption": "none"}
        if vnext_flow is not None:
            user_payload["flow"] = vnext_flow

        settings_payload["vnext"] = [{"address": vnext_server, "port": vnext_port, "users": [user_payload]}]

    if mode == "flattened":
        expected = VlessOutbound(
            tag=tag,
            server=flat_server,
            server_port=flat_port,
            uuid=flat_user_id,
            flow=flat_flow,
        )
    else:
        expected = VlessOutbound(
            tag=tag,
            server=vnext_server,
            server_port=vnext_port,
            uuid=vnext_user_id,
            flow=vnext_flow,
        )

    payload = {"protocol": "vless", "tag": tag, "settings": settings_payload}

    return payload, expected


@st.composite
def invalid_xray_vless_payload(draw):
    host_alphabet = ascii_lowercase + digits + "-."
    tag_alphabet = ascii_lowercase + digits + "-_"

    server = draw(_safe_text(host_alphabet, min_size=4, max_size=32))
    server_port = draw(st.integers(min_value=1, max_value=65535))
    tag = draw(_safe_text(tag_alphabet, min_size=1, max_size=24))
    user_id = str(draw(st.uuids()))
    invalid_case = draw(
        st.sampled_from(
            [
                "invalid_port",
                "invalid_uuid",
                "empty_vnext",
                "empty_users",
                "missing_encryption",
                "missing_id",
                "missing_address",
            ]
        )
    )

    settings_payload: dict[str, object] = {"protocol": "vless"}

    match invalid_case:
        case "invalid_port":
            settings_payload.update({"address": server, "port": 0, "id": user_id, "encryption": "none"})
        case "invalid_uuid":
            settings_payload.update({"address": server, "port": server_port, "id": "not-a-uuid", "encryption": "none"})
        case "empty_vnext":
            settings_payload["vnext"] = []
        case "empty_users":
            settings_payload["vnext"] = [{"address": server, "port": server_port, "users": []}]
        case "missing_encryption":
            settings_payload.update({"address": server, "port": server_port, "id": user_id})
        case "missing_id":
            settings_payload.update({"address": server, "port": server_port, "encryption": "none"})
        case "missing_address":
            settings_payload.update({"port": server_port, "id": user_id, "encryption": "none"})

    payload: dict[str, object] = {"protocol": "vless", "tag": tag, "settings": settings_payload}

    return payload


@st.composite
def valid_xray_hysteria_payload(draw):
    host_alphabet = ascii_lowercase + digits + "-."
    tag_alphabet = ascii_lowercase + digits + "-_"
    password_alphabet = ascii_lowercase + digits + "-_@"

    server = draw(_safe_text(host_alphabet, min_size=4, max_size=32))
    server_port = draw(st.integers(min_value=1, max_value=65535))
    tag = draw(_safe_text(tag_alphabet, min_size=1, max_size=24))
    password = draw(_safe_text(password_alphabet, min_size=1, max_size=32))
    insecure = draw(st.one_of(st.none(), st.booleans()))

    stream_settings: dict[str, object] = {
        "network": "hysteria",
        "hysteriaSettings": {"auth": password},
    }
    expected_tls = None
    if insecure is not None:
        stream_settings["hysteriaSettings"] = {"auth": password, "masquerade": {"insecure": insecure}}
        expected_tls = TlsOptions(insecure=insecure)

    payload = {
        "protocol": "hysteria",
        "tag": tag,
        "settings": {"protocol": "hysteria", "address": server, "port": server_port},
        "streamSettings": stream_settings,
    }

    return payload, Hysteria2Outbound(
        tag=tag,
        server=server,
        server_port=server_port,
        password=password,
        tls=expected_tls,
    )


@st.composite
def invalid_xray_hysteria_payload(draw):
    host_alphabet = ascii_lowercase + digits + "-."
    tag_alphabet = ascii_lowercase + digits + "-_"
    password_alphabet = ascii_lowercase + digits + "-_@"

    server = draw(_safe_text(host_alphabet, min_size=4, max_size=32))
    server_port = draw(st.integers(min_value=1, max_value=65535))
    tag = draw(_safe_text(tag_alphabet, min_size=1, max_size=24))
    password = draw(_safe_text(password_alphabet, min_size=1, max_size=32))
    invalid_case = draw(
        st.sampled_from(
            [
                "invalid_port",
                "missing_stream_settings",
                "wrong_network",
                "missing_hysteria_settings",
                "missing_auth",
            ]
        )
    )

    settings_payload: dict[str, object] = {"protocol": "hysteria", "address": server, "port": server_port}
    payload: dict[str, object] = {"protocol": "hysteria", "tag": tag, "settings": settings_payload}

    if invalid_case == "invalid_port":
        settings_payload["port"] = 0
    elif invalid_case == "missing_stream_settings":
        pass
    elif invalid_case == "wrong_network":
        payload["streamSettings"] = {"network": "grpc", "hysteriaSettings": {"auth": password}}
    elif invalid_case == "missing_hysteria_settings":
        payload["streamSettings"] = {"network": "hysteria"}
    elif invalid_case == "missing_auth":
        payload["streamSettings"] = {"network": "hysteria", "hysteriaSettings": {"masquerade": {"insecure": True}}}

    return payload


@given(valid_xray_vless_payload())
@settings(max_examples=400)
def test_from_xray_on_generated_valid_vless_payloads(payload_and_expected):
    payload, expected = payload_and_expected

    outbound = from_xray(json.dumps(payload))

    assert isinstance(outbound, VlessOutbound)
    assert outbound == expected
    assert outbound.security is None
    assert outbound.transport is None


@given(invalid_xray_vless_payload())
@settings(max_examples=400)
def test_from_xray_on_generated_invalid_vless_payloads(payload):
    with pytest.raises(ValueError):
        from_xray(json.dumps(payload))


@given(valid_xray_hysteria_payload())
@settings(max_examples=300)
def test_from_xray_on_generated_valid_hysteria_payloads(payload_and_expected):
    payload, expected = payload_and_expected

    outbound = from_xray(json.dumps(payload))

    assert isinstance(outbound, Hysteria2Outbound)
    assert outbound == expected


@given(invalid_xray_hysteria_payload())
@settings(max_examples=300)
def test_from_xray_on_generated_invalid_hysteria_payloads(payload):
    with pytest.raises(ValueError):
        from_xray(json.dumps(payload))
