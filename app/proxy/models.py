from typing import Any

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class ProxyProvider(Base, kw_only=True):
    __tablename__ = "proxy_providers"

    name: Mapped[str] = mapped_column(primary_key=True)
    proxies: Mapped[list[Proxy]] = relationship(
        back_populates="provider", cascade="all, delete-orphan", passive_deletes=True
    )


class Proxy(Base, kw_only=True, omit_defaults=True):
    __tablename__ = "proxies"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    xray_config: Mapped[dict[str, Any]] = mapped_column(JSON)
    provider_name: Mapped[str] = mapped_column(ForeignKey("proxy_providers.name", ondelete="CASCADE"))

    provider: Mapped[ProxyProvider] = relationship(back_populates="proxies", init=False)
