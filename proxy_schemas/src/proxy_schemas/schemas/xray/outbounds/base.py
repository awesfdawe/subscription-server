from ..base import XrayBase
from ..stream_settings import StreamSettings


class Outbound(XrayBase, tag_field="protocol"):
    tag: str
    stream_settings: StreamSettings
