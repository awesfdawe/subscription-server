class OutboundError(ValueError):
    message: str = "An outbound error occurred"

    def __init__(self, message: str | None = None, *args: object) -> None:
        super().__init__(self.message if message is None else message, *args)


class URIValidationError(OutboundError):
    message: str = "URI validation failed"


class MissingHostError(URIValidationError):
    message: str = "The hostname is missing from the URI"


class MissingPortError(URIValidationError):
    message: str = "The port is missing from the URI"


class MissingTagError(URIValidationError):
    message: str = "The tag is missing from the URI"


class MissingCredentialsError(URIValidationError):
    message: str = "The password is missing from the URI"


class MissingPublicKeyError(URIValidationError):
    message: str = "The URI contains the reality parameter but lacks a public key"


class UnsupportedProtocolError(URIValidationError):
    message: str = "The string is not an outbound URI, or the library does not yet support this protocol"


class InvalidURIError(URIValidationError):
    message: str = "The string is not a valid URI"
