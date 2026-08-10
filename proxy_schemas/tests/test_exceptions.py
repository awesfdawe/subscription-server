import pytest
from proxy_schemas.exceptions import (
    ConfigParseError,
    ConfigValidationError,
    OutboundConversionError,
    UnsupportedProtocolError,
)
from proxy_schemas.schemas.singbox.outbounds.base import Outbound as SingboxOutbound
from proxy_schemas.schemas.xray.outbounds.base import Outbound as XrayOutbound
from proxy_schemas.schemas.xray.outbounds.vless import VlessOutbound as XrayVlessOutbound
from proxy_schemas.schemas.xray.outbounds.vless import VlessSettings, VlessVnext


class DummyUnsupportedXrayOutbound(XrayOutbound, tag="unsupported_proto"):
    pass


class DummyUnsupportedSingboxOutbound(SingboxOutbound, tag="unsupported_proto"):
    pass


def test_invalid_json_raises_config_parse_error(adapter):
    with pytest.raises(ConfigParseError, match="Invalid JSON"):
        adapter.get_xray_outbounds("invalid json {{")

    with pytest.raises(ConfigParseError, match="Invalid JSON"):
        adapter.get_singbox_outbounds("{broken json")


def test_non_dict_root_raises_config_parse_error(adapter):
    with pytest.raises(ConfigParseError, match="Expected a JSON object"):
        adapter.get_xray_outbounds("[1, 2, 3]")

    with pytest.raises(ConfigParseError, match="Expected a JSON object"):
        adapter.get_singbox_outbounds('"string_root"')


def test_outbounds_not_list_raises_config_parse_error(adapter):
    with pytest.raises(ConfigParseError, match="Expected 'outbounds' to be a list"):
        adapter.get_xray_outbounds({"outbounds": "not_a_list"})

    with pytest.raises(ConfigParseError, match="Expected 'outbounds' to be a list"):
        adapter.get_singbox_outbounds({"outbounds": 12345})


def test_validation_error_raises_config_validation_error(adapter):
    # Missing required 'tag' or 'protocol'
    invalid_outbound_config = {"outbounds": [{"protocol": "vless", "settings": {}}]}
    with pytest.raises(ConfigValidationError):
        adapter.get_xray_outbounds(invalid_outbound_config)


def test_missing_server_params_raises_outbound_conversion_error(adapter):
    empty_settings = VlessSettings()
    bad_xray_node = XrayVlessOutbound(label="bad", settings=empty_settings)
    with pytest.raises(OutboundConversionError, match="missing required server parameters"):
        adapter.xray_to_singbox(bad_xray_node)


def test_empty_vnext_users_raises_outbound_conversion_error(adapter):
    empty_vnext = VlessVnext(address="1.1.1.1", port=443, users=[])
    legacy_empty_users = VlessSettings(vnext=[empty_vnext])
    bad_xray_node = XrayVlessOutbound(label="bad_vnext", settings=legacy_empty_users)
    with pytest.raises(OutboundConversionError, match="vnext\\[0\\].users list is empty"):
        adapter.xray_to_singbox(bad_xray_node)


def test_unsupported_protocol_raises_unsupported_error(adapter):
    unsupported_xray = DummyUnsupportedXrayOutbound(label="unsupported")
    with pytest.raises(UnsupportedProtocolError, match="Xray protocol"):
        adapter.xray_to_singbox(unsupported_xray)

    unsupported_sb = DummyUnsupportedSingboxOutbound(tag="unsupported", server="1.1.1.1", server_port=443)
    with pytest.raises(UnsupportedProtocolError, match="Singbox outbound type"):
        adapter.singbox_to_xray(unsupported_sb)
