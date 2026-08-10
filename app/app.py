from litestar import Litestar, get

from app.config import get_config
from app.logging import setup_logging

setup_logging()
config = get_config()


@get("/")
async def get_subscription() -> str:
    return "test"


app = Litestar([get_subscription])
