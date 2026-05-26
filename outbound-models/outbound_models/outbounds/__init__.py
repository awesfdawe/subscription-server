from typing import Union

from .vless import VlessOutbound
from .hysteria2 import Hysteria2Outbound

AnyOutbound = Union[VlessOutbound, Hysteria2Outbound]
