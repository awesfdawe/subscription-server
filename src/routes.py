from litestar import get

from src.config import get_config


@get("{user_prefix:str}")
async def get_subscription(user_prefix: str) -> str:
    config = get_config()
    for user in config.users.values():
        if user.url_prefix == user_prefix:
            return f"test {user_prefix}"
    return "not allowed"