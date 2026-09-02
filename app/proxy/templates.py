import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import msgspec

from app.files import get_file_content


@lru_cache(1)
def get_xray_template(template_path: Path) -> dict[str, Any]:
    try:
        return get_file_content(template_path, "json", dict[str, Any])
    except OSError, msgspec.MsgspecError:
        sys.exit(1)


@lru_cache(1)
def get_mihomo_template(template_path: Path) -> dict[str, Any]:
    try:
        return get_file_content(template_path, "yaml", dict[str, Any])
    except OSError, msgspec.MsgspecError:
        sys.exit(1)


def merge_with_xray_template(config: dict[str, Any], template: dict[str, Any]) -> dict[str, Any]:
    merged = config | template
    if template.get("routing") and config.get("routing"):
        merged["routing"] = config["routing"] | template["routing"]
    if template.get("outbounds") and config.get("outbounds"):
        merged["outbounds"] = config["outbounds"] + template["outbounds"]
    return merged
