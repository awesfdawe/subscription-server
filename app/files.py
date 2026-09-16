from pathlib import Path
from typing import Any, Literal

import msgspec
from loguru import logger


def _dec_hook(type_: type, obj: Any) -> Any:
    if type_ is Path:
        return Path(obj)
    raise NotImplementedError


def get_file_content[T = Any](
    file_path: Path,
    file_format: Literal["yaml", "json"],
    validation_type: type[T],
) -> T:
    try:
        with file_path.open(mode="rb") as f:
            file_content = f.read()
    except OSError as e:
        logger.critical(f"Error accessing file {file_path}: {e}")
        raise

    try:
        if file_format == "yaml":
            return msgspec.yaml.decode(file_content, type=validation_type, dec_hook=_dec_hook)
        if file_format == "json":
            return msgspec.json.decode(file_content, type=validation_type, dec_hook=_dec_hook)
    except msgspec.MsgspecError as e:
        logger.critical(f"File decoding/validation error in {file_path}: {e}")
        raise
