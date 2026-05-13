from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from functools import lru_cache


class Settings(BaseSettings):
    environment: Literal["dev", "prod"] = "dev"

    database_url: str = "sqlite:///db.sqlite3"

    jwt_secret: str = "changeitinprod"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
