class OutboundError(ValueError):
    pass


class UriValidationError(OutboundError):
    pass


class MissingHostnameError(UriValidationError):
    pass


class MissingPortError(UriValidationError):
    pass


class MissingTagError(UriValidationError):
    pass


class MissingPasswordError(UriValidationError):
    pass


class MissingPublicKeyError(UriValidationError):
    pass


class NotSupportedError(UriValidationError):
    pass


class InvalidUri(UriValidationError):
    pass
