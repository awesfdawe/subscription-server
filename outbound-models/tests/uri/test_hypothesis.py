from hypothesis import given, strategies as st

from outbound_models.models.outbounds.vless import VlessOutbound
from outbound_models.models.outbounds.hysteria2 import Hysteria2Outbound
from outbound_models.models.outbounds import AnyOutbound

from outbound_models.adapters.uri import to_uri

hysteria_st = st.from_type(Hysteria2Outbound)
vless_st = st.from_type(VlessOutbound)

outbound_strategy = st.one_of(vless_st, hysteria_st)
@given(outbound_strategy)
def test_to_uri_on_hypothesis(outbound: AnyOutbound) -> None:
    to_uri(outbound)