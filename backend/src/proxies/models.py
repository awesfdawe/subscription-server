from sqlmodel import Field, SQLModel, Relationship, Column, JSON, AutoString
from typing import List

from src.proxies.types.bundle import ProxyConfig
from src.proxies.types.protocols import protocols


class ProxyProvider(SQLModel, table=True):
    __tablename__ = "proxy_providers"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=40)
    show_name: bool

    servers: List[Proxy] = Relationship(back_populates="provider")


class Proxy(SQLModel, table=True):
    __tablename__ = "proxies"

    id: int | None = Field(default=None, primary_key=True)
    original_name: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=40)

    protocol: protocols = Field(sa_type=AutoString)
    server: str = Field(max_length=1000)
    port: int = Field(gt=0, le=65535)

    config_data: dict = Field(default_factory=dict, sa_column=Column(JSON))

    provider_id: int = Field(foreign_key="proxy_providers.id")

    provider: ProxyProvider = Relationship(back_populates="servers")

    @property
    def config(self) -> ProxyConfig:
        return ProxyConfig.model_validate(self.config_data)

    @config.setter
    def config(self, config: ProxyConfig):
        self.config_data = config.model_dump(by_alias=True, exclude_none=True)
