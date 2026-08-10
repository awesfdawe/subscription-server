from proxy_schemas.schemas.base import SchemaBase


class XrayBase(SchemaBase, rename="camel", kw_only=True):
    pass
