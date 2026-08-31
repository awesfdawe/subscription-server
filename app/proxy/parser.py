from typing import Any

import msgspec
from aiohttp import ClientError, ClientSession, ClientTimeout
from loguru import logger
from sqlalchemy import delete

from app.database import Database
from app.proxy.models import Proxy, ProxyProvider
from app.proxy.schemas import XraySchema


def get_validated_xray_configs(xray_configs: list[dict[str, Any]]) -> list[XraySchema]:
    ignored_protocols = ("freedom", "blackhole", "dns", "loopback")

    validated_configs = []
    for config in xray_configs:
        try:
            valid_config = msgspec.convert(config, type=XraySchema)
            valid_config.outbounds = [
                outbound for outbound in valid_config.outbounds if outbound.get("protocol") not in ignored_protocols
            ]
            validated_configs.append(valid_config)
        except msgspec.ValidationError as e:
            logger.error(f"Non valid xray json config: {e}")

    return validated_configs


async def dump_xray_subscription(
    provider_name: str,
    url: str,
    headers: dict[str, str] | None,
    min_proxies: int,
    db: Database,
):
    try:
        async with (
            ClientSession() as session,
            session.get(url, headers=headers, timeout=ClientTimeout(15.0)) as response,
        ):
            response.raise_for_status()
            response_text = await response.text()
    except (ClientError, TimeoutError) as e:
        logger.error(f"Request to {url} failed: {e}")
        return

    try:
        xray_configs = msgspec.json.decode(response_text, type=list[dict[str, Any]])
    except msgspec.DecodeError as e:
        logger.error(f"Request returned non valid json response: {e}")
        return

    validated_configs = get_validated_xray_configs(xray_configs)

    validated_configs_len = len(validated_configs)
    if validated_configs_len >= min_proxies:
        db_proxies = [
            Proxy(xray_config=msgspec.to_builtins(config), provider_name=provider_name) for config in validated_configs
        ]
        async with db.session_factory() as db_session:
            provider = await db_session.get(ProxyProvider, provider_name)
            if provider:
                await db_session.execute(delete(Proxy).where(Proxy.provider_name == provider_name))
                db_session.add_all(db_proxies)
            else:
                provider = ProxyProvider(
                    name=provider_name,
                    proxies=db_proxies,
                )
                db_session.add(provider)

            await db_session.commit()
            logger.info(f"Xray configs of provider: {provider_name} dumped successfuly")
    else:
        logger.error(f"Request returned less xray configs than was requied: {validated_configs_len} < {min_proxies}")
