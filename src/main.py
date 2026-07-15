import msgspec
from litestar import Litestar, get, Request, Response

from src.config import config
from src.client import proxy_client
from src.modifiers import singbox_modify


@get(f"{config.forward.path}/{{short_uuid:str}}")
async def get_subscription(request: Request, short_uuid: str) -> Response:
    response = await proxy_client.forward_get(f"{config.forward.path}/{short_uuid}", request)
    response_headers = response.headers
    match response_headers.get("Content-Type"):
        case "application/json":
            try:
                data = dict(msgspec.json.decode(response.text))  # TODO: Reuse decoder
            except msgspec.DecodeError as e:
                print(f"decoding errror: {e}")  # TODO: Proper logging

            if data.get("routing"):
                content = response.text
                # TODO: Add modifications (xray). Need to impelemnt to_xray method in outbound_models
            elif data.get("route"):
                content = msgspec.json.encode(singbox_modify(data))  # TODO: Reuse encoder

        case "text/yaml":
            try:
                data = dict(msgspec.yaml.decode(response.text))  # TODO: Reuse decoder
            except msgspec.DecodeError as e:
                print(f"decoding errror: {e}")  # TODO: Proper logging

            # TODO: Continue here

        case _:
            content = response.text

    return Response(
        content=content, status_code=response.status_code, headers=response_headers, cookies=response.cookies
    )


app = Litestar(route_handlers=[get_subscription])
