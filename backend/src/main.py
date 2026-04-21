from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings

import src.auth.router as auth


api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)


settings = get_settings()

if settings.environment == "dev":
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app = FastAPI(docs_url=None, redoc_url=None)

app.include_router(api_router)
