from typing import Any


def _get_param(xray_json: dict[str, Any], key: str) -> Any | None:
    values = xray_json.get(key)
    return values[0] if values else None
