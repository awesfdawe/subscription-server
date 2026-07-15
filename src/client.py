import httpx
from litestar import Request

from src.config import config


class ProxyClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=config.forward.timeout)

    async def close(self) -> None:
        await self.client.aclose()

    async def forward_get(self, path: str | None, request: Request) -> httpx.Response:

        headers = dict(request.headers)
        headers.pop("host", None)

        return await self.client.get(
            f"http://{config.forward.domain}/{path}",
            headers=headers,
            params=request.query_params,
            cookies=request.cookies,
        )


proxy_client = ProxyClient()
