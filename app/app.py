import asyncio
import sys
from contextlib import asynccontextmanager
from typing import Any

import aiofiles
import msgspec
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from litestar import Litestar, Response, get
from litestar.datastructures import State
from litestar.exceptions import NotFoundException
from loguru import logger
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.config import Config, get_config
from app.database import Database
from app.logging import setup_logging
from app.proxy.models import ProxyProvider
from app.proxy.parser import dump_xray_subscription
from app.proxy.templates import get_xray_template
from app.users import Users, get_users_inital, watch_users_file

setup_logging()
config = get_config()


@get(f"{config.app.path_prefix}{{user_path:str}}")
async def get_subscription(state: State, user_path: str) -> Response[list[dict[str, Any]]]:
    users: Users = state.users
    if user_path in (user.path_prefix for user in users.users.values()):
        db: Database = state.db
        stmt = select(ProxyProvider).options(selectinload(ProxyProvider.proxies))
        async with db.session_factory() as db_session:
            result = await db_session.execute(stmt)

        config: Config = state.config
        xray_template: dict[str, Any] = state.xray_template

        providers = result.scalars().all()
        subscription = []

        for provider_name, provider in config.proxy_providers.items():
            if provider.show_title and provider.title:
                subscription.append(
                    {"outbounds": [{"protocol": "blackhole", "tag": "block"}], "remarks": provider.title}
                )
            if provider.type == "url":
                for db_provider in providers:
                    if db_provider.name == provider_name:
                        for proxy in db_provider.proxies:
                            merged = proxy.xray_config | xray_template
                            if "routing" in xray_template and "routing" in proxy.xray_config:
                                merged["routing"] = proxy.xray_config["routing"] | xray_template["routing"]
                            if "outbounds" in xray_template and "outbounds" in proxy.xray_config:
                                merged["outbounds"] = proxy.xray_config["outbounds"] + xray_template["outbounds"]
                            subscription.append(merged)
            elif provider.type == "file":
                try:
                    async with aiofiles.open(provider.path, encoding="utf-8") as f:
                        file_content = await f.read()
                except FileNotFoundError:
                    logger.critical(f"File does not exist at path: {provider.path}")
                    sys.exit(1)
                except IsADirectoryError:
                    logger.critical(f"Path is a directory, not a file: {provider.path}")
                    sys.exit(1)
                except PermissionError:
                    logger.critical(f"Permission denied when reading file: {provider.path}")
                    sys.exit(1)

                try:
                    xray_config = msgspec.json.decode(file_content)
                    merged = xray_config | xray_template
                    if "routing" in xray_template and "routing" in xray_config:
                        merged["routing"] = xray_config["routing"] | xray_template["routing"]
                    if "outbounds" in xray_template and "outbounds" in xray_config:
                        merged["outbounds"] = xray_config["outbounds"] + xray_template["outbounds"]
                    subscription.append(merged)
                except msgspec.ValidationError as e:
                    logger.critical(f"Users file validation error: {e}")
                    sys.exit(1)

        return Response(subscription, headers=config.app.response_headers)
    raise NotFoundException()


@asynccontextmanager
async def lifespan(app: Litestar):
    app.state.config = config
    app.state.users = await get_users_inital(config.app.users_file_path)
    app.state.xray_template = get_xray_template(config.app.xray_template_path)

    db = Database(f"sqlite+aiosqlite:///{config.app.proxy_db_path}")

    providers_names = list(config.proxy_providers.keys())
    async with db.session_factory() as session:
        if providers_names:
            stmt = delete(ProxyProvider).where(ProxyProvider.name.not_in(providers_names))
        else:
            stmt = delete(ProxyProvider)

        await session.execute(stmt)
        await session.commit()

    scheduler = AsyncIOScheduler()

    for name, provider in config.proxy_providers.items():
        if provider.type == "url" and provider.url is not None:
            async with db.session_factory() as db_session:
                db_provider = await db_session.get(ProxyProvider, name, options=[selectinload(ProxyProvider.proxies)])
                if (
                    not db_provider
                    or len(db_provider.proxies) < provider.min_proxies
                    or config.app.update_proxies_on_start
                ):
                    await dump_xray_subscription(name, provider.url, provider.headers, provider.min_proxies, db)

            scheduler.add_job(
                dump_xray_subscription,
                "interval",
                seconds=provider.update_interval,
                id=name,
                args=[name, provider.url, provider.headers, provider.min_proxies, db],
            )

    scheduler.start()

    app.state.db = db

    watcher_task = None
    if config.app.watch_users_file:
        watcher_task = asyncio.create_task(watch_users_file(app))

    try:
        yield
    finally:
        if watcher_task is not None:
            watcher_task.cancel()
            await asyncio.gather(watcher_task, return_exceptions=True)
        await db.dispose()
        scheduler.shutdown(wait=False)


app = Litestar([get_subscription], lifespan=[lifespan], debug=True)
