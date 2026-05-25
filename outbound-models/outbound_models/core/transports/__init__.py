from typing import Union

from .grpc import GrpcTransport
from .ws import WebsocketTransport

AnyTransport = Union[GrpcTransport, WebsocketTransport]
