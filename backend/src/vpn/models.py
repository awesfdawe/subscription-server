from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List


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
