import sys
from functools import lru_cache
from os import getenv
from pathlib import Path
from typing import Annotated, Literal

import msgspec

from app.files import get_file_content


def get_config_dir() -> Path:
    return Path("/config") if Path("/config").is_dir() else Path("config")


def get_data_dir() -> Path:
    return Path("/data") if Path("/data").is_dir() else Path("data")


def default_users_path() -> Path:
    return get_config_dir() / "users.yaml"


def default_db_path() -> Path:
    return get_data_dir() / "db.sqlite3"


def default_xray_template_path() -> Path:
    return get_config_dir() / "xray_template.json"


class AppConfig(msgspec.Struct):
    bind: str = "0.0.0.0"
    port: int = 8000
    trusted_ips: list[str] | str | None = None
    response_headers: dict[str, str] | None = None
    unix_socket_path: str | None = None
    users_file_path: Path = msgspec.field(default_factory=default_users_path)
    proxy_db_path: Path = msgspec.field(default_factory=default_db_path)
    xray_template_path: Path = msgspec.field(default_factory=default_xray_template_path)
    path_prefix: str = "/"
    watch_users_file: bool = False
    update_proxies_on_start: bool = False

    def __post_init__(self):
        if not self.path_prefix[0] == "/" and self.path_prefix[-1] == "/":
            raise ValueError("Path prefix should start with / and end with /. Example: '/sub/', '/'")

        if self.response_headers:
            for key, value in self.response_headers.items():
                if not key.isascii() or not value.isascii():
                    raise ValueError("Response headers can't contain non-ascii symbols")

        self.proxy_db_path.parent.mkdir(parents=True, exist_ok=True)


class ProxyProvider(msgspec.Struct):
    title: str | None = None
    show_title: bool = True
    type: Literal["url", "file"] | None = None
    url: str | None = None
    headers: dict[str, str] | None = None
    update_interval: Annotated[int, msgspec.Meta(ge=30)] = 43200
    min_proxies: Annotated[int, msgspec.Meta(ge=1)] = 5
    path: str | None = None

    def __post_init__(self):
        if self.type == "url" and self.url is None:
            raise ValueError("url must be specified when type = url")
        if self.type == "file" and self.path is None:
            raise ValueError("path must be specified when type = file")


class Config(msgspec.Struct):
    proxy_providers: dict[str, ProxyProvider]
    app: AppConfig = msgspec.field(default_factory=AppConfig)


@lru_cache(1)
def get_config() -> Config:
    config_path = Path(getenv("CONFIG_PATH", get_config_dir() / "config.yaml"))
    try:
        return get_file_content(config_path, "yaml", Config)
    except OSError, msgspec.MsgspecError:
        sys.exit(1)
