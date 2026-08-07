from hypothesis import HealthCheck, given, settings
from proxy_schemas.schemas.singbox.transports.grpc import GrpcTransport as SingboxGrpcTransport
from proxy_schemas.schemas.singbox.transports.websocket import WebsocketTransport as SingboxWebsocketTransport

from tests.strategies import singbox_vless_st, xray_vless_flat_st, xray_vless_legacy_st


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(node=xray_vless_flat_st())
def test_xray_flat_field_mapping(adapter, node):
    sb = adapter.xray_to_singbox(node)
    assert sb.tag == node.tag
    assert sb.server == node.settings.address
    assert sb.server_port == node.settings.port
    assert sb.uuid == node.settings.id


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(node=xray_vless_legacy_st())
def test_xray_legacy_field_mapping(adapter, node):
    sb = adapter.xray_to_singbox(node)
    vnext = node.settings.vnext[0]
    user = vnext.users[0]
    assert sb.tag == node.tag
    assert sb.server == vnext.address
    assert sb.server_port == vnext.port
    assert sb.uuid == user.id


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(node=singbox_vless_st())
def test_singbox_field_mapping(adapter, node):
    xray = adapter.singbox_to_xray(node)
    assert xray.tag == node.tag
    assert xray.settings.address == node.server
    assert xray.settings.port == node.server_port
    assert xray.settings.id == node.uuid

    if node.tls and node.tls.enabled:
        assert xray.stream_settings is not None
        if node.tls.reality and node.tls.reality.enabled:
            assert xray.stream_settings.reality_settings is not None
            assert xray.stream_settings.reality_settings.public_key == node.tls.reality.public_key
            assert xray.stream_settings.reality_settings.short_id == node.tls.reality.short_id

    if isinstance(node.transport, SingboxWebsocketTransport):
        assert xray.stream_settings is not None
        assert xray.stream_settings.ws_settings is not None
        assert xray.stream_settings.ws_settings.path == node.transport.path
    elif isinstance(node.transport, SingboxGrpcTransport):
        assert xray.stream_settings is not None
        assert xray.stream_settings.grpc_settings is not None
        assert xray.stream_settings.grpc_settings.service_name == node.transport.service_name
