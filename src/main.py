from granian.constants import Interfaces
from granian import Granian
import msgspec
from base64 import b64decode, b64encode
from litestar import Litestar, get, Request, Response

from src.config import config
from src.msgspec import json_encoder, json_decoder
from src.client import proxy_client
from src.modifiers import singbox_modify, xray_modify, mihomo_modify, base64_modify


@get(f"/{config.forward.path}/{{short_uuid:str}}")
async def get_subscription(request: Request, short_uuid: str) -> Response:
    response = await proxy_client.forward_get(f"{config.forward.path}/{short_uuid}", request)

    response_headers = response.headers
    response_headers.pop("content-length", None)
    response_headers.pop("content-encoding", None)

    match response_headers.get("Content-Type"):
        case "text/plain":
            data = b64decode(response.text).decode()

            content = b64encode(base64_modify(data).encode())

        case "application/json":
            try:
                data = dict(json_decoder.decode(response.text))
            except msgspec.DecodeError as e:
                print(f"decoding errror: {e}")  # TODO: Proper logging

            if data.get("routing"):
                content = json_encoder.encode(xray_modify(data))
            elif data.get("route"):
                content = json_encoder.encode(singbox_modify(data))

        case "text/yaml":
            try:
                data = dict(msgspec.yaml.decode(response.text))
            except msgspec.DecodeError as e:
                print(f"decoding errror: {e}")  # TODO: Proper logging

            content = msgspec.yaml.encode(mihomo_modify(data))

        case _:
            content = response.content

    return Response(
        content=content, status_code=response.status_code, headers=response_headers, cookies=response.cookies
    )


@get(["/{path:path}"])
async def forward_else(request: Request, path: str = "") -> Response:
    response = await proxy_client.forward_get(path, request)

    response_headers = response.headers
    response_headers.pop("content-length", None)
    response_headers.pop("content-encoding", None)

    return Response(
        content=response.content, status_code=response.status_code, headers=response_headers, cookies=response.cookies
    )


app = Litestar(route_handlers=[get_subscription, forward_else])


if __name__ == "__main__":
    server = Granian(
        target="src.main:app",
        address="0.0.0.0",
        port=8000,
        interface=Interfaces.ASGI,
    )
    server.serve()
