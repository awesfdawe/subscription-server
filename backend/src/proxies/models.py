from sqlmodel import Field, SQLModel, Relationship, Column, JSON
from typing import List

from .types.bundle import ProxyConfig


class ProxyProviders(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=40)
    show_name: bool

    servers: List[Proxies] = Relationship(back_populates="provider")


class Proxies(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_name: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=40)

    protocol: str
    server: str
    port: int

    config_data: dict = Field(default_factory=dict, sa_column=Column(JSON))

    provider_id: int = Field(foreign_key="proxyproviders.id")

    provider: ProxyProviders = Relationship(back_populates="servers")

    @property
    def config(self) -> ProxyConfig:
        return ProxyConfig.model_validate(self.config_data)

    @config.setter
    def config(self, config: ProxyConfig):
        self.config_data = config.model_dump(by_alias=True, exclude_none=True)
