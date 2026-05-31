from .vless import VlessOutbound
from .hysteria2 import Hysteria2Outbound

AnyOutbound = VlessOutbound | Hysteria2Outbound
