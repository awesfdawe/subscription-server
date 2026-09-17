import logging
import re
import sys
from contextlib import asynccontextmanager
from copy import deepcopy
from os import getenv
from pathlib import Path
from typing import Any, Literal

import msgspec
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from litestar import Litestar, Request, Response, get
from litestar.datastructures import State
from litestar.exceptions import NotFoundException
from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from app.config import Config, get_config
from app.database import Database
from app.files import get_file_content
from app.proxy.converters.xray_to_mihomo import multi_xray_configs_to_mihomo
from app.proxy.models import ProxyProvider
from app.proxy.parser import dump_xray_subscription, get_validated_xray_configs
from app.proxy.schemas.xray import XrayConfigSchema
from app.proxy.templates import get_mihomo_template, get_xray_template, merge_with_xray_template
from app.users import get_users

config = get_config()


@get([f"{config.app.path_prefix}{{user_path:str}}/{{client_type:str}}", f"{config.app.path_prefix}{{user_path:str}}"])
async def get_subscription(
    state: State, request: Request, user_path: str, client_type: Literal["xray", "mihomo"] | None = None
) -> Response[bytes] | Response[list[dict[str, Any]]]:
    users_prefixes: set[str] = state.users_prefixes
    if user_path in users_prefixes:
        db: Database = state.db
        stmt = select(ProxyProvider).options(selectinload(ProxyProvider.proxies))
        async with db.session_factory() as db_session:
            result = await db_session.execute(stmt)

        config: Config = state.config
        providers = result.scalars().all()
        file_providers: dict[str, list[XrayConfigSchema]] = state.file_providers
        if client_type is None:
            user_agent = request.headers.get("user-agent", "")
            client_type = "mihomo" if state.mihomo_ua_regex.search(user_agent) else "xray"

        if client_type == "mihomo":
            xray_configs: list[XrayConfigSchema] = []
            for provider_name, provider in config.proxy_providers.items():
                if provider.type == "url":
                    for db_provider in providers:
                        if db_provider.name == provider_name:
                            for proxy in db_provider.proxies:
                                xray_configs.append(msgspec.convert(proxy.xray_config, type=XrayConfigSchema))
                elif provider.type == "file" and provider_name in file_providers:
                    xray_configs.extend(file_providers[provider_name])

            outbounds = multi_xray_configs_to_mihomo(xray_configs)

            mihomo_template: dict[str, Any] = deepcopy(state.mihomo_template)
            mihomo_template["proxies"] = outbounds
            for group in mihomo_template.get("proxy-groups", []):
                if group.get("proxies") is None:
                    group["proxies"] = [outbound.name for outbound in outbounds]

            return Response(
                msgspec.yaml.encode(mihomo_template),
                headers=config.app.response_headers,
                media_type="application/yaml",
            )
        if client_type == "xray":
            xray_template: dict[str, Any] = state.xray_template
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
                                subscription.append(merge_with_xray_template(proxy.xray_config, xray_template))
                elif provider.type == "file":
                    for proxy in file_providers[provider_name]:
                        subscription.append(merge_with_xray_template(msgspec.to_builtins(proxy), xray_template))

            return Response(
                subscription,
                headers=config.app.response_headers,
            )
    raise NotFoundException()


@asynccontextmanager
async def lifespan(app: Litestar):
    app.state.config = config
    users = get_users(config.app.users_file_path)
    app.state.users = users
    app.state.users_prefixes = {user.path_prefix for user in users.users.values()}
    app.state.xray_template = get_xray_template(config.app.xray_template_path)
    app.state.mihomo_template = get_mihomo_template(config.app.mihomo_template_path)
    app.state.mihomo_ua_regex = re.compile(config.app.mihomo_ua_regex, re.IGNORECASE)

    config.app.proxy_db_path.parent.mkdir(parents=True, exist_ok=True)
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

    file_providers = {}

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
        elif provider.type == "file":
            try:
                file_providers[name] = get_validated_xray_configs(
                    get_file_content(Path(provider.path), "json", list[dict[str, Any]])  # ty: ignore[invalid-argument-type]
                )
            except OSError, msgspec.MsgspecError:
                sys.exit(1)

    app.state.file_providers = file_providers

    scheduler.start()

    app.state.db = db

    try:
        yield
    finally:
        await db.dispose()
        scheduler.shutdown(wait=False)


debug_ = False
if logging.getLevelNamesMapping().get(getenv("LOG_LEVEL"), logging.INFO) == 10:
    debug_ = True
app = Litestar([get_subscription], lifespan=[lifespan], debug=debug_)
