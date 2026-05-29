from outbound_models import Outbound

outbound = Outbound.from_uri(
    "vless://00000000-0000-0000-0000-000000000000@example.com:8443?type=tcp&security=reality&flow=xtls-rprx-vision&fp=chrome&pbk=0000000000000000000000000000000000000000000&sid=0000000000000000&sni=example.com#vless%20reality%20vision%20tcp%202"
)

print(outbound.to_uri())
