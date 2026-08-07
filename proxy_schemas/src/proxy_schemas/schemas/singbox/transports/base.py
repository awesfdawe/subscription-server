from proxy_schemas.schemas.base import SchemaBase


class Transport(SchemaBase, kw_only=True, forbid_unknown_fields=True):
    pass
