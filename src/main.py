from outbound_models import Outbound

outbound = Outbound.from_uri(
    "hysteria2://letmein@example.com:123,5000-6000/?insecure=1&obfs=salamander&obfs-password=gawrgura&pinSHA256=deadbeef&sni=real.example.com#test"
)

print(outbound)
