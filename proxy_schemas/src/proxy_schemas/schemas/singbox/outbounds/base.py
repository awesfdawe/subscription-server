from proxy_schemas.schemas.base import SchemaBase
from proxy_schemas.schemas.types import Port


class Outbound(SchemaBase):
    tag: str
    server: str
    server_port: Port
