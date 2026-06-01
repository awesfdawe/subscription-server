import msgspec


class BaseProtocol(msgspec.Struct, tag_field="protocol"):
    pass
