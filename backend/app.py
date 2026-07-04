from __future__ import annotations

from pathlib import Path

from litestar import Litestar
from litestar.middleware.session.client_side import CookieBackendConfig
from litestar_vite import InertiaConfig, PathConfig, RuntimeConfig, TypeGenConfig, ViteConfig, VitePlugin

from backend.config import DEV_MODE, FRONTEND_DIR, SECRET_KEY
from backend.controllers.pages import PagesController


session_backend = CookieBackendConfig(secret=SECRET_KEY.encode("utf-8"))

vite = VitePlugin(
    config=ViteConfig(
        dev_mode=DEV_MODE,
        paths=PathConfig(root=FRONTEND_DIR, resource_dir="resources"),
        inertia=InertiaConfig(),
        types=TypeGenConfig(output=Path("resources/generated")),
        runtime=RuntimeConfig(port=5173),
    )
)

app = Litestar(
    route_handlers=[PagesController],
    plugins=[vite],
    middleware=[session_backend.middleware],
    debug=True,
)
