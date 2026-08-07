from proxy_schemas.schemas.singbox.outbounds.vless import (
    Flows as SingboxFlows,
)
from proxy_schemas.schemas.singbox.outbounds.vless import (
    VlessOutbound as SingboxVlessOutbound,
)
from proxy_schemas.schemas.xray.outbounds.vless import (
    Flows as XrayFlows,
)
from proxy_schemas.schemas.xray.outbounds.vless import (
    VlessOutbound as XrayVlessOutbound,
)
from proxy_schemas.schemas.xray.outbounds.vless import (
    VlessSettings,
)

from ..stream_settings import (
    singbox_to_xray_stream_settings,
    xray_stream_settings_to_singbox_tls,
    xray_stream_settings_to_singbox_transport,
)


def xray_vless_to_singbox(data: XrayVlessOutbound) -> SingboxVlessOutbound:
    settings = data.settings
    if settings.address is not None and settings.port is not None and settings.id is not None:
        server = settings.address
        server_port = settings.port
        uuid = settings.id
        raw_flow = settings.flow
    elif settings.vnext:
        vnext = settings.vnext[0]
        if not vnext.users:
            raise ValueError("Legacy VlessSettings users list is empty")
        user = vnext.users[0]
        server = vnext.address
        server_port = vnext.port
        uuid = user.id
        raw_flow = user.flow
    else:
        raise ValueError("VlessSettings is missing required server parameters")

    flow: SingboxFlows | None = None
    if raw_flow is not None:
        try:
            flow = SingboxFlows(str(raw_flow))
        except ValueError:
            flow = None

    tls = xray_stream_settings_to_singbox_tls(data.stream_settings)
    transport = xray_stream_settings_to_singbox_transport(data.stream_settings)

    return SingboxVlessOutbound(
        tag=data.tag,
        server=server,
        server_port=server_port,
        uuid=uuid,
        flow=flow,
        tls=tls,
        transport=transport,
    )


def singbox_vless_to_xray(data: SingboxVlessOutbound) -> XrayVlessOutbound:
    flow: XrayFlows | None = None
    if data.flow is not None:
        try:
            flow = XrayFlows(data.flow.value)
        except ValueError:
            flow = None

    settings = VlessSettings(
        address=data.server,
        port=data.server_port,
        id=data.uuid,
        encryption="none",
        flow=flow,
    )

    stream_settings = singbox_to_xray_stream_settings(data.tls, data.transport)

    return XrayVlessOutbound(
        tag=data.tag,
        settings=settings,
        stream_settings=stream_settings,
    )
