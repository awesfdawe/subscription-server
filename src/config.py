from functools import lru_cache
import os
from pathlib import Path
from typing import Annotated
import msgspec


class UnixSocketConfig(msgspec.Struct, frozen=True):
    path: Path
    permissions: str = "0660"


class AppConfig(msgspec.Struct, frozen=True):
    url_prefix: str
    unix_socket: UnixSocketConfig | None = None
    address: str = "0.0.0.0"
    port: Annotated[int, msgspec.Meta(ge=1, le=65535)] = 8000


class ProxyProviderConfig(msgspec.Struct, frozen=True):
    subscription_url: str
    headers: dict[str, str] | None = None
    update_interval: int = 43200


class UserConfig(msgspec.Struct, frozen=True):
    url_prefix: str


class Config(msgspec.Struct, frozen=True):
    app: AppConfig
    users: dict[str, UserConfig]
    # proxies: dict[str, ProxyProviderConfig]


@lru_cache(1)
def get_config() -> Config:
    path = Path(os.getenv("CONFIG_PATH", "config.yaml"))
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {path.absolute()}")

    with open(path, "rb") as f:
        return msgspec.yaml.decode(f.read(), type=Config)
