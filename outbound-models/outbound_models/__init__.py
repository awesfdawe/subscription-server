from outbound_models.adapters import uri as uri_adapter
from outbound_models.models.outbounds import AnyOutbound


class Outbound:
    @staticmethod
    def from_uri(uri: str) -> AnyOutbound:
        return uri_adapter.from_uri(uri)

    def to_uri(self) -> str:
        return self.to_uri()
