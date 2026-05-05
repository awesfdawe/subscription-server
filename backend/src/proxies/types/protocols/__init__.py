from typing import Union
from .vless import VlessSettings
from .hysteria2 import Hysteria2Settings
from .shadowsocks import ShadowsocksSettings

ProtocolsConfig = Union[VlessSettings, Hysteria2Settings, ShadowsocksSettings]
