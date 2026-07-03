from .hysteria2 import Hysteria2Singbox
from .vless import VlessSingbox

AnyOutboundSingbox = VlessSingbox | Hysteria2Singbox
