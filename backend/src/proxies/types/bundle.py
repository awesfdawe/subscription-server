from pydantic import BaseModel, Field
from typing import Annotated, Optional

from .protocols import ProtocolsConfig
from .security import SecurityConfig
from .transports import TransportConfig


class ProxyConfig(BaseModel):
    protocol_settings: Annotated[ProtocolsConfig, Field(discriminator="protocol")]
    security_settings: Optional[Annotated[SecurityConfig, Field(discriminator="security")]]
    transport_settings: Optional[Annotated[TransportConfig, Field(discriminator="transport")]]
