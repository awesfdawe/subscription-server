import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import msgspec
from loguru import logger


@lru_cache(1)
def get_xray_template(template_path: Path) -> dict[str, Any]:
    try:
        file_content = template_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.critical(f"File does not exist at path: {template_path.absolute()}")
        sys.exit(1)
    except IsADirectoryError:
        logger.critical(f"Path is a directory, not a file: {template_path.absolute()}")
        sys.exit(1)
    except PermissionError:
        logger.critical(f"Permission denied when reading file: {template_path.absolute()}")
        sys.exit(1)

    try:
        return msgspec.json.decode(file_content, type=dict[str, Any])
    except msgspec.ValidationError as e:
        logger.critical(f"Xray template validation error: {e}")
        sys.exit(1)
