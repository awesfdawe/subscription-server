from outbound_models.models.transports.grpc import GrpcTransport


def from_uri(query: dict[str, list[str]]) -> GrpcTransport:
    service_name = query.get("serviceName", [None])[0]

    return GrpcTransport(service_name=service_name)


def to_uri(grpc: GrpcTransport) -> dict[str, str]:
    query_params = {}

    if grpc.service_name:
        query_params.update({"serviceName": grpc.service_name})

    return query_params
