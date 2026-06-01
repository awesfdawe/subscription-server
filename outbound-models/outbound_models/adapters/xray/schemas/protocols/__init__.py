from .vless import VlessProtocol
from .hysteria2 import Hysteria2Protocol

AnyProtocol = VlessProtocol | Hysteria2Protocol
