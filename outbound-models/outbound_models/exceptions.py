class OutboundError(Exception):
    message: str = "An outbound error occurred"

    def __str__(self) -> str:
        if self.args:
            details = ", ".join(str(arg) for arg in self.args)
            return f"{self.message}: {details}"

        return self.message


class InputValidationError(OutboundError):
    message: str = "Input data did not pass validation"


class InputParsingError(OutboundError):
    message: str = "Input data is malformed or could not be parse"


class MissingParameterError(OutboundError):
    message: str = "Required parameter is missing from the input data"


class UnsupportedProtocolError(OutboundError):
    message: str = "Library does not yet support this protocol"
