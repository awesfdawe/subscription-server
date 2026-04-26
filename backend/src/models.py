from sqlalchemy import String
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List

SQLModel.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Admins(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=30)
    hashed_password: str = Field(sa_type=String(255))


class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=3, max_length=40)
    description: str = Field(default="", max_length=400)
    expire_time: datetime
    enabled: bool = Field(default=True)


class VPNProviders(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=40)
    show_name: bool

    servers: List["VPNServers"] = Relationship(back_populates="provider")


class VPNServers(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    original_name: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=40)
    link: str = Field(min_length=1, max_length=2000)

    provider_id: int | None = Field(default=None, foreign_key="vpnproviders.id")

    provider: Optional[VPNProviders] = Relationship(back_populates="servers")

    # protocol: Literal["vless", "vmess", "trojan", "ss", "hy2"]
    # address: str = Field(min_length=1, max_length=255)
    # port: int = Field(ge=1, le=65535)
    # settings: dict[str, Any] = Field(default_factory=dict, sa_column=Column(MutableDict.as_mutable(JSON)))
    # @property
    # def typed_settings(self):
    #     match self.protocol:
    #         case "vless":
    #             return VlessSettings(**self.settings)
    #         case "vmess":
    #             return VmessSettings(**self.settings)
    #         case "trojan":
    #             return TrojanSettings(**self.settings)
    #         case "ss":
    #             return ShadowsocksSettings(**self.settings)
    #         case "hy2":
    #             return Hysteria2Settings(**self.settings)
    #         case _:
    #             raise ValueError(f"Unknown protocol: {self.protocol}")
