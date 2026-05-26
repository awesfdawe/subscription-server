from .base import BaseTransport


class Hysteria2Transport(BaseTransport, tag="hysteria2"):
    password: str
