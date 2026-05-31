from outbound_models.models.security.tls import TlsSecurity
from outbound_models.models.security import AnySecurity

from . import tls


def _to_uri(transport: AnySecurity) -> dict[str, str]:
    match transport:
        case TlsSecurity():
            return tls._to_uri(transport)
