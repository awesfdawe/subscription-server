from urllib.parse import urlencode, urlunsplit, SplitResult
import pytest
from pathlib import Path
from hypothesis import given, strategies as st

from outbound_models.adapters.uri import from_uri
from outbound_models.models.outbounds import AnyOutbound

fake_valid_links_path = Path(__file__).parent.parent / "test_data" / "fake_valid_links.txt"


def get_valid_links() -> list[str]:
    with open(fake_valid_links_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


@pytest.fixture(params=get_valid_links())
def valid_link(request: pytest.FixtureRequest):
    return request.param


def test_from_uri_on_valid_links(valid_link: str):
    outbound = from_uri(valid_link)

    assert isinstance(outbound, AnyOutbound)
    assert outbound.server
    assert outbound.server_port
    assert outbound.tag


@st.composite
def generated_valid_link(draw):
    scheme = draw(st.sampled_from(["vless", "hysteria2"]))
    uuid = draw(st.uuids())
    host = draw(st.just("example.com"))
    port = draw(st.integers(min_value=1, max_value=65535))

    match scheme:
        case "vless":
            possible_params = {
                "security": ["none", "tls", "reality"],
                "flow": ["xtls-rprx-vision", "xtls-rprx-vision-udp443", "none"],
                "type": ["tcp", "raw", "xhttp", "ws", "grpc"],
                "sni": ["google.com", "github.com", "microsoft.com"],
                "pbk": ["public_key_1", "public_key_2"],
                "sid": ["shortid1", "shortid2"],
                "insecure": ["0", "1"],
            }
        case "hysteria2":
            possible_params = {
                "insecure": ["0", "1"],
                "sni": ["google.com", "microsoft.com"],
            }

    available_keys = list(possible_params.keys())
    selected_keys = draw(
        st.lists(st.sampled_from(available_keys), unique=True, min_size=0, max_size=len(available_keys))
    )

    query_dict = {}
    for key in selected_keys:
        allowed_values = possible_params[key]
        query_dict[key] = draw(st.sampled_from(allowed_values))

    query = urlencode(query_dict)

    return urlunsplit(
        SplitResult(scheme=scheme, netloc=f"{uuid}@{host}:{port}", path="", query=query, fragment="example")
    )


@given(generated_valid_link())
def test_from_uri_on_generated_valid_links(generated_valid_link: str):
    outbound = from_uri(generated_valid_link)

    assert isinstance(outbound, AnyOutbound)
    assert outbound.server
    assert outbound.server_port
    assert outbound.tag
