from outbound_models.adapters import uri as uri_adapter


class Outbound:
    def __init__(self, inner):
        self._inner = inner

    @classmethod
    def from_uri(cls, uri_string: str) -> "Outbound":
        inner_struct = uri_adapter.parse(uri_string)
        return cls(inner_struct)

    def __getattr__(self, name: str):
        return getattr(self._inner, name)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(inner={self._inner!r})"
