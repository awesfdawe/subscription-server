from granian.constants import Interfaces
from granian import Granian
from litestar import Litestar

from src.config import get_config
from src.routes import get_subscription

config = get_config()

app = Litestar(route_handlers=[get_subscription], path=config.app.url_prefix)

if __name__ == "__main__":
    if config.app.unix_socket:
        server = Granian(
            target="src.main:app",
            uds=config.app.unix_socket.path,
            uds_permissions=int(config.app.unix_socket.permissions, 8),
            interface=Interfaces.ASGI,
        )
    else:
        server = Granian(
            target="src.main:app",
            address=str(config.app.address),
            port=config.app.port,
            interface=Interfaces.ASGI,
        )

    server.serve()
