from pydantic import BaseModel, Field
from typing import Annotated

from .protocols import ProtocolsConfig
from .security import SecurityConfig
from .transports import TransportConfig


class ProxyConfig(BaseModel):
    protocol_settings: Annotated[ProtocolsConfig, Field(discriminator="protocol")]
    security_settings: Annotated[SecurityConfig, Field(discriminator="security")] | None
    transport_settings: Annotated[TransportConfig, Field(discriminator="transport")] | None
