from proxy_schemas.schemas.base import SchemaBase
from proxy_schemas.schemas.types import Port


class Outbound(SchemaBase, tag_field="type", kw_only=True, forbid_unknown_fields=True):
    tag: str
    server: str
    server_port: Port
