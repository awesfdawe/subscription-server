from hypothesis import given, provisional as st

from outbound_models import Outbound
from outbound_models.exceptions import OutboundError


@given(st.urls())
def test_from_uri_on_hyphothesis_urls(link: str) -> None:
    try:
        Outbound.from_uri(link)
    except OutboundError:
        pass
