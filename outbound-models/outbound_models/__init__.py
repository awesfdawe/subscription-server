from outbound_models.adapters import uri as uri_adapter
from outbound_models.outbounds import AnyOutbound


class Outbound:
    @staticmethod
    def from_uri(uri_string: str) -> AnyOutbound:
        return uri_adapter.parse(uri_string)

