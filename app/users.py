import sys
from functools import lru_cache
from pathlib import Path

import msgspec

from app.files import get_file_content


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


@lru_cache(1)
def get_users(file_path: Path) -> Users:
    try:
        return get_file_content(file_path, "yaml", Users)
    except OSError, msgspec.MsgspecError:
        sys.exit(1)
