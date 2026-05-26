import pytest
from pathlib import Path

from outbound_models import Outbound
from outbound_models.outbounds import AnyOutbound

fixture_path = Path(__file__).parent / "fixtures" / "fake_valid_links.txt"

def get_valid_links() -> list[str]:
    with open(fixture_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

@pytest.fixture(params=get_valid_links())
def link(request: pytest.FixtureRequest):
    return request.param

def test_links(link: str) -> None:
    outbound = Outbound.from_uri(link)

    assert isinstance(outbound, AnyOutbound)
    assert outbound.server is not None
    assert outbound.server_port is not None
    assert outbound.tag is not None