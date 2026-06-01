import msgspec


class BaseProtocolXray(msgspec.Struct, tag_field="protocol", kw_only=True):
    pass
