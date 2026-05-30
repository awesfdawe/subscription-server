class OutboundError(ValueError):
    """Base exception for all outbound-related errors."""

    message: str = "An outbound error occurred"

    def __init__(self, message: str | None = None, *args: object) -> None:
        super().__init__(self.message if message is None else message, *args)


class URIValidationError(OutboundError):
    """Base exception for URI validation errors."""

    message: str = "URI validation failed"


class MissingHostError(URIValidationError):
    """Raised when the hostname is missing from the URI."""

    message: str = "The hostname is missing from the URI"


class MissingPortError(URIValidationError):
    """Raised when the port is missing from the URI."""

    message: str = "The port is missing from the URI"


class MissingTagError(URIValidationError):
    """Raised when the tag is missing from the URI."""

    message: str = "The tag is missing from the URI"


class MissingCredentialsError(URIValidationError):
    """Raised when the password, UUID, or credentials are missing from the URI."""

    message: str = "The password is missing from the URI"


class MissingPublicKeyError(URIValidationError):
    """Raised when the public key is missing from the URI."""

    message: str = "The URI contains the reality parameter but lacks a public key"


class UnsupportedProtocolError(URIValidationError):
    """Raised when the protocol is not supported."""

    message: str = "The string is not an outbound URI, or the library does not yet support this protocol"


class InvalidURIError(URIValidationError):
    """Raised when the URI is invalid."""

    message: str = "The string is not a valid URI"
