from outbound_models.schemas.xray import XrayConfig
from outbound_models.schemas.xray.protocols.hysteria2 import Hysteria2Xray
from outbound_models.models.outbounds.hysteria2 import Hysteria2Outbound, TlsOptions


def _from_xray(xray: XrayConfig) -> Hysteria2Outbound:
    settings = xray.settings

    match settings:
        case Hysteria2Xray():
            pass
        case _:
            raise ValueError("Wrong settings")

    hysteria_settings = None
    stream = xray.stream_settings
    if stream:
        match stream.network:
            case "hysteria":
                if stream.hysteria_settings:
                    hysteria_settings = stream.hysteria_settings
                else:
                    raise ValueError("Hysteria2 settings is missing from xray json")

    if not hysteria_settings:
        raise ValueError("Hysteria2 auth is missing from xray json")

    tls = None
    if hysteria_settings.masquerade:
        tls = TlsOptions(insecure=hysteria_settings.masquerade.insecure)

    return Hysteria2Outbound(
        server=settings.address, server_port=settings.port, tag=xray.tag, password=hysteria_settings.auth, tls=tls
    )
