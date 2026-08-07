class ProxySchemaError(Exception):
    """Base exception for all proxy_schemas library errors."""


class ConfigParseError(ProxySchemaError):
    """Raised when the raw config cannot be parsed (invalid JSON, wrong root type, etc.)."""


class ConfigValidationError(ProxySchemaError):
    """Raised when the config structure is valid JSON but does not match the expected schema."""


class OutboundConversionError(ProxySchemaError):
    """Raised when an outbound cannot be converted due to missing or inconsistent fields."""


class UnsupportedProtocolError(ProxySchemaError):
    """Raised when an outbound protocol is not yet implemented in the adapter."""
