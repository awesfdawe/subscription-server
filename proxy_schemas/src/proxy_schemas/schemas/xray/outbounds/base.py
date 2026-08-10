import msgspec

from ..base import XrayBase
from ..stream_settings import StreamSettings


class Outbound(XrayBase, tag_field="protocol"):
    label: str | None = msgspec.field(default=None, name="tag")
    stream_settings: StreamSettings | None = None
