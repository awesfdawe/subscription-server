from contextlib import asynccontextmanager

from aiohttp import ClientSession
from litestar import Litestar, get
from sqlalchemy import delete

from app.config import get_config
from app.database import Database
from app.logging import setup_logging
from app.proxy.models import ProxyProvider
from app.proxy.parser import dump_xray_subscription

setup_logging()
config = get_config()


@get("/")
async def get_subscription() -> str:
    return "test"


@asynccontextmanager
async def lifespan(app: Litestar):
    db = Database(f"sqlite+aiosqlite:///{config.app.proxy_db_path}")

    providers_names = list(config.proxy_providers.keys())

    async with db.session_factory() as session:
        if providers_names:
            stmt = delete(ProxyProvider).where(ProxyProvider.name.not_in(providers_names))
        else:
            stmt = delete(ProxyProvider)

        await session.execute(stmt)
        await session.commit()

    async with ClientSession() as session:
        for name, provider in config.proxy_providers.items():
            if provider.url is not None:
                await dump_xray_subscription(name, provider.url, provider.headers, provider.mix_proxies, db, session)

    app.state.db = db

    try:
        yield
    finally:
        await db.dispose()


app = Litestar([get_subscription], lifespan=[lifespan])
