from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal
from functools import lru_cache


class Settings(BaseSettings):
    environment: Literal["dev", "prod"] = Field("dev")

    database_url: str = Field("sqlite:///db.sqlite3")

    jwt_secret: str = Field("changeitinprod")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
