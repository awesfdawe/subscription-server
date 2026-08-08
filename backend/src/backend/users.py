import asyncio
import sys
from pathlib import Path

import aiofiles
import msgspec
from litestar import Litestar
from watchfiles import awatch

from backend.config import get_config
from backend.logging import get_logger


class User(msgspec.Struct):
    path_prefix: str


class Users(msgspec.Struct):
    users: dict[str, User]

    def __post_init__(self):
        prefixes = set()

        for user_key, user in self.users.items():
            if user.path_prefix in prefixes:
                raise ValueError(f"Duplicate path_prefix '{user.path_prefix}' found for user '{user_key}'")

        prefixes.add(user.path_prefix)


async def get_users_inital(file_path: Path) -> Users:
    logger = get_logger(__name__)

    try:
        async with aiofiles.open(file_path, encoding="utf-8") as f:
            file_content = await f.read()
    except FileNotFoundError:
        logger.critical(f"File does not exist at path: {file_path}")
        sys.exit(1)
    except IsADirectoryError:
        logger.critical(f"Path is a directory, not a file: {file_path}")
        sys.exit(1)
    except PermissionError:
        logger.critical(f"Permission denied when reading file: {file_path}")
        sys.exit(1)

    try:
        return msgspec.yaml.decode(file_content, type=Users)
    except msgspec.ValidationError as e:
        logger.critical(f"Config validation error: {e}")
        sys.exit(1)


async def get_users(file_path: Path) -> Users:
    async with aiofiles.open(file_path, encoding="utf-8") as f:
        file_content = await f.read()
    return msgspec.yaml.decode(file_content, type=Users)


async def watch_users_file(app: Litestar) -> None:
    logger = get_logger(__name__)

    config = get_config()
    file_path = Path(config.app.users_file_path)

    try:
        async for _ in awatch(file_path):
            try:
                app.state.users = await get_users(file_path)
                logger.info("Users file reloaded successfully")
            except (OSError, msgspec.ValidationError, msgspec.DecodeError, ValueError) as e:
                logger.error(f"Failed to reload users file '{file_path}': {e}")

    except asyncio.CancelledError:
        pass
