from enum import StrEnum
from typing import Annotated

from msgspec import Meta

Port = Annotated[int, Meta(ge=0, le=65535)]


class TlsVersion(StrEnum):
    V1_0 = "1.0"
    V1_1 = "1.1"
    V1_2 = "1.2"
    V1_3 = "1.3"
