import sys
from functools import lru_cache
from os import getenv
from pathlib import Path
from typing import Annotated

import msgspec
from loguru import logger


class AppConfig(msgspec.Struct):
    bind: str = "0.0.0.0"
    port: int = 8000
    response_headers: dict[str, str] | None = None
    users_file_path: str = "users.yaml"
    proxy_db_path: str = "db.sqlite3"
    xray_template_path: str | None = None
    path_prefix: str = "/sub/"
    watch_users_file: bool = False
    update_proxies_on_start: bool = False

    def __post_init__(self):
        if not self.path_prefix[0] == "/" and self.path_prefix[-1] == "/":
            raise ValueError("Path prefix should start with / and end with /. Example: '/sub/'")


class ProxyProvider(msgspec.Struct):
    title: str | None = None
    show_title: bool = True
    url: str | None = None
    headers: dict[str, str] | None = None
    update_interval: Annotated[int, msgspec.Meta(ge=30)] = 43200
    min_proxies: Annotated[int, msgspec.Meta(ge=1)] = 5


class Config(msgspec.Struct):
    proxy_providers: dict[str, ProxyProvider]
    app: AppConfig = msgspec.field(default_factory=AppConfig)


@lru_cache(1)
def get_config() -> Config:
    config_path = getenv("CONFIG_PATH")
    file_path = Path(config_path) if config_path is not None else Path("config.yaml")
    try:
        file_content = file_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        logger.critical(f"File does not exist at path: {file_path.absolute()}")
        sys.exit(1)
    except IsADirectoryError:
        logger.critical(f"Path is a directory, not a file: {file_path.absolute()}")
        sys.exit(1)
    except PermissionError:
        logger.critical(f"Permission denied when reading file: {file_path.absolute()}")
        sys.exit(1)

    try:
        return msgspec.yaml.decode(file_content, type=Config)
    except msgspec.ValidationError as e:
        logger.critical(f"Config validation error: {e}")
        sys.exit(1)
