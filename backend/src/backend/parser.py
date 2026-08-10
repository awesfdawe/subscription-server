import aiohttp
import msgspec
from proxy_schemas.adapters.adapter import OutboundAdapter
from proxy_schemas.exceptions import ConfigParseError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.logging import get_logger
from backend.models import Proxy, ProxyProvider


async def parse_subscription(
    provider_name: str,
    url: str,
    headers: dict[str, str] | None,
    min_proxies: int,
    adapter: OutboundAdapter,
    session_factory: async_sessionmaker[AsyncSession],
):
    logger = get_logger(__name__)
    async with aiohttp.ClientSession() as session, session.get(url, headers=headers) as response:
        raw_config = await response.text()
        logger.warning(raw_config)
    try:
        outbounds = adapter.get_xray_outbounds(raw_config)
    except ConfigParseError as e:
        logger.error(f"Error occured when getting outbounds: {e}")
        return

    logger.info(f"Sucessfully retrieved outbounds from {provider_name}")

    outbounds_len = len(outbounds)
    if outbounds_len >= min_proxies:
        proxies = [Proxy(outbound=msgspec.to_builtins(outbound)) for outbound in outbounds]

        provider = ProxyProvider(name=provider_name, proxies=proxies)

        async with session_factory() as session:
            await session.merge(provider)
            await session.commit()
    else:
        logger.warning(
            f"Len of retrieved otbounds from {provider_name} меньше чем нужно ({outbounds_len} < {min_proxies})"
        )
