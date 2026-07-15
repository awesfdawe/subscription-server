from base64 import b64decode, b64encode


def base64_modify(base64_sub: bytes) -> bytes:
    data = b64decode(base64_sub).decode()

    data = data.join(
        [
            "vless://00000000-0000-0000-0000-000000000000@example.com:444?type=tcp&security=reality&pbk=0000000000000000000000000000000000000000000&fp=chrome&sni=example.com&sid=00000000&spx=%2F&flow=xtls-rprx-vision#vless%20reality%20vision%20tcp%201"
        ]
    )

    return b64encode(data.encode())


def xray_modify(xray_sub: dict) -> dict:
    outbounds = xray_sub.get("outbounds")

    if outbounds is None:
        # TODO: add log
        return xray_sub

    outbounds = dict(outbounds)

    # outbounds.update() TODO: add to_xray here

    xray_sub["outbounds"] = outbounds

    return xray_sub


def singbox_modify(singbox_sub: dict) -> dict:
    outbounds = singbox_sub.get("outbounds")

    if outbounds is None:
        # TODO: add log
        return singbox_sub

    outbounds = dict(outbounds)

    outbounds.update()  # TODO: add to_singbox here

    return singbox_sub
