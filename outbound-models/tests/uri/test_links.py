import pytest
from pathlib import Path
from urllib.parse import unquote

from outbound_models import Outbound
from outbound_models.models.outbounds import AnyOutbound

fixture_path = Path(__file__).parent / "fixtures" / "fake_valid_links.txt"


def get_valid_links() -> list[str]:
    with open(fixture_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


@pytest.fixture(params=get_valid_links(), ids=lambda link: unquote(link.split("#")[-1]) if "#" in link else link[:30])
def link(request: pytest.FixtureRequest):
    return request.param


def test_from_uri_on_valid_links(link: str) -> None:
    outbound = Outbound.from_uri(link)

    assert isinstance(outbound, AnyOutbound)
    assert outbound.server
    assert outbound.server_port
    assert outbound.tag
