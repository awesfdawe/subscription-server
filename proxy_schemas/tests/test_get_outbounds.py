import json

import msgspec
from hypothesis import given
from hypothesis import strategies as st
from proxy_schemas.schemas.singbox.outbounds.vless import VlessOutbound as SingboxVlessOutbound
from proxy_schemas.schemas.xray.outbounds.vless import VlessOutbound as XrayVlessOutbound

from tests.strategies import singbox_vless_st, xray_vless_flat_st


@given(nodes=st.lists(xray_vless_flat_st(), min_size=1, max_size=5))
def test_get_xray_outbounds_from_dict_and_str(adapter, nodes):
    builtins_nodes = [msgspec.to_builtins(n) for n in nodes]
    config_dict = {"outbounds": builtins_nodes}

    res_dict = adapter.get_xray_outbounds(config_dict)
    assert len(res_dict) == len(nodes)
    assert all(isinstance(n, XrayVlessOutbound) for n in res_dict)

    config_str = json.dumps(config_dict)
    res_str = adapter.get_xray_outbounds(config_str)
    assert len(res_str) == len(nodes)
    assert all(isinstance(n, XrayVlessOutbound) for n in res_str)


@given(nodes=st.lists(singbox_vless_st(), min_size=1, max_size=5))
def test_get_singbox_outbounds_from_dict_and_str(adapter, nodes):
    builtins_nodes = [msgspec.to_builtins(n) for n in nodes]
    config_dict = {"outbounds": builtins_nodes}

    res_dict = adapter.get_singbox_outbounds(config_dict)
    assert len(res_dict) == len(nodes)
    assert all(isinstance(n, SingboxVlessOutbound) for n in res_dict)

    config_str = json.dumps(config_dict)
    res_str = adapter.get_singbox_outbounds(config_str)
    assert len(res_str) == len(nodes)
    assert all(isinstance(n, SingboxVlessOutbound) for n in res_str)
