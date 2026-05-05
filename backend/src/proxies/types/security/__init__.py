from typing import Union
from .tls import TlsSettings
from .reality import RealitySettings

SecurityConfig = Union[TlsSettings, RealitySettings]
