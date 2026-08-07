from hypothesis import HealthCheck, given, settings

from tests.strategies import singbox_vless_st, xray_vless_any_st


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(node=singbox_vless_st())
def test_singbox_xray_singbox_roundtrip(adapter, node):
    xray_node = adapter.singbox_to_xray(node)
    sb_node = adapter.xray_to_singbox(xray_node)
    assert sb_node == node


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(node=xray_vless_any_st())
def test_xray_singbox_xray_singbox_roundtrip(adapter, node):
    sb1 = adapter.xray_to_singbox(node)
    xray2 = adapter.singbox_to_xray(sb1)
    sb2 = adapter.xray_to_singbox(xray2)
    assert sb1 == sb2
