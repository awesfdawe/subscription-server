def base64_modify(base64_sub: str) -> str:
    base64_sub += "\n".join(["update here"])
    return base64_sub


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

    # outbounds.update() TODO: add to_singbox here

    singbox_sub["outbounds"] = outbounds

    return singbox_sub


def mihomo_modify(mihomo_sub: dict) -> dict:
    outbounds = mihomo_sub.get("proxies")

    if outbounds is None:
        # TODO: add log
        return mihomo_sub

    outbounds = dict(outbounds)

    # outbounds.update() TODO: add to_mihomo here

    mihomo_sub["proxies"] = outbounds

    return mihomo_sub
