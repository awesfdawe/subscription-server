import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from litestar import Litestar, Request, get
from litestar.datastructures import State
from litestar.di import Provide
from proxy_schemas.adapters.adapter import OutboundAdapter
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import get_config
from backend.database import DatabaseHelper, db_session
from backend.logging import get_logging_config
from backend.models import ProxyProvider
from backend.parser import parse_subscription
from backend.users import Users, get_users_inital, watch_users_file

config = get_config()


@get(
    f"{config.app.path_prefix}{{user_path:str}}",
    dependencies={"db_session": Provide(db_session)},
)
async def get_subscription(request: Request, state: State, db_session: AsyncSession, user_path: str) -> None:
    request.logger.info(user_path)
    users_db: Users = state.users
    if user_path in (user.path_prefix for user in users_db.users.values()):
        # result = await db_session.execute(select(ProxyProvider))
        # proxy_providers = result.scalars().all()
        # for provider in proxy_providers:
        #     for proxy in provider.proxies:
        #         proxy.outbound
        # request.logger.info(str(proxy_providers))
        pass


@asynccontextmanager
async def lifespan(app: Litestar):
    users_file_path = Path(config.app.users_file_path)
    app.state.users = await get_users_inital(users_file_path)

    db_url = f"sqlite+aiosqlite:///{config.app.proxy_db_path}"
    db_helper = DatabaseHelper(db_url=db_url)

    providers_names = list(config.proxy_providers.keys())

    async with db_helper.session_factory() as session:
        if providers_names:
            stmt = delete(ProxyProvider).where(ProxyProvider.name.not_in(providers_names))
        else:
            stmt = delete(ProxyProvider)

        await session.execute(stmt)
        await session.commit()

    adapter = OutboundAdapter()

    for name, provider in config.proxy_providers.items():
        if provider.url is not None:
            await parse_subscription(
                name, provider.url, provider.headers, provider.mix_proxies, adapter, db_helper.session_factory
            )

    app.state.db_helper = db_helper

    watcher_task = None
    if config.app.watch_users_file:
        watcher_task = asyncio.create_task(watch_users_file(app))

    try:
        yield
    finally:
        if watcher_task is not None:
            watcher_task.cancel()
            await asyncio.gather(watcher_task, return_exceptions=True)
        await db_helper.dispose()


app = Litestar(
    route_handlers=[get_subscription],
    logging_config=get_logging_config(),
    lifespan=[lifespan],
)
