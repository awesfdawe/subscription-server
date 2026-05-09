from urllib.parse import ParseResult

from src.proxies.models import Proxies
from src.proxies.types.bundle import ProxyConfig


def parse(parsed: ParseResult, query: dict, name: str) -> Proxies:
    flat_data = {"uuid": parsed.username, **query}

    network_type = query.get("type", "tcp")
    security_type = query.get("security", "none")

    raw_config = {
        "protocol_settings": {"protocol": "vless", **flat_data},
    }

    raw_config["transport_settings"] = {"transport": network_type, **flat_data}

    if security_type != "none":
        raw_config["security_settings"] = {"security": security_type, **flat_data}

    db_proxy = Proxies(original_name=name, name=name, protocol="vless", server=parsed.hostname, port=parsed.port)
    db_proxy.config = ProxyConfig.model_validate(raw_config)

    return db_proxy
