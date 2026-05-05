from sqlmodel import Field, SQLModel, Relationship
from typing import List


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

    # config:

    provider_id: int = Field(foreign_key="proxyproviders.id")

    provider: ProxyProviders = Relationship(back_populates="servers")
