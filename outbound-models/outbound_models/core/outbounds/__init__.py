from typing import Union

from .vless import VlessOutbound
from .hysteria2 import Hysteria2Protocol

AnyOutbound = Union[VlessOutbound, Hysteria2Protocol]
