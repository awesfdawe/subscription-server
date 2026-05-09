from typing import Union, Literal
from .vless import VlessSettings
from .hysteria2 import Hysteria2Settings
from .shadowsocks import ShadowsocksSettings

ProtocolsConfig = Union[VlessSettings, Hysteria2Settings, ShadowsocksSettings]

protocols = Literal["vless", "hysteria2", "shadowsocks"]
