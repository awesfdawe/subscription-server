from hypothesis import given, provisional as st

from outbound_models.adapters.uri import from_uri
from outbound_models.exceptions import OutboundError


@given(st.urls())
def test_from_uri_on_hyphothesis_urls(link: str) -> None:
    try:
        from_uri(link)
    except OutboundError:
        pass
