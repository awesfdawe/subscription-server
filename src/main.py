from outbound_models.adapters.uri import to_uri, from_uri

outbound = from_uri(
    "hysteria2://letmein@example.com:123,5000-6000/?insecure=1&obfs=salamander&obfs-password=gawrgura&pinSHA256=deadbeef&sni=real.example.com#test"
)

print(outbound)

print(to_uri(outbound))