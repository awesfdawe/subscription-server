from litestar import Litestar, Request, get

from backend.logging import get_logging_config


@get("/")
async def my_router_handler(request: Request) -> None:
    request.logger.info("test")


app = Litestar(route_handlers=[my_router_handler], logging_config=get_logging_config())
