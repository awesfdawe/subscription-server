from proxy_schemas.schemas.base import SchemaBase


class XrayBase(SchemaBase, rename="camel", kw_only=True, forbid_unknown_fields=True):
    pass
