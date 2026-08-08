import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from litestar import Litestar, Request, get
from litestar.datastructures import State

from backend.config import get_config
from backend.logging import get_logging_config
from backend.users import Users, get_users_inital, watch_users_file

config = get_config()


@get(f"{config.app.path_prefix}{{user_path:str}}")
async def get_subscription(request: Request, state: State, user_path: str) -> None:
    request.logger.info(user_path)
    users_db: Users = state.users
    if user_path in (user.path_prefix for user in users_db.users.values()):
        request.logger.info("Subscription given")


@asynccontextmanager
async def lifespan(app: Litestar):
    users_file_path = Path(config.app.users_file_path)
    app.state.users = await get_users_inital(users_file_path)

    watcher_task = asyncio.create_task(watch_users_file(app))
    try:
        yield
    finally:
        watcher_task.cancel()
        await asyncio.gather(watcher_task, return_exceptions=True)


app = Litestar(route_handlers=[get_subscription], logging_config=get_logging_config(), lifespan=[lifespan])
