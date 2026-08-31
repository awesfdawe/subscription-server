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
