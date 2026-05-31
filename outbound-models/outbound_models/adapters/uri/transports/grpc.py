from outbound_models.models.transports.grpc import GrpcTransport

from ..utils import _get_param


def _from_uri(query: dict[str, list[str]]) -> GrpcTransport:
    return GrpcTransport(service_name=_get_param(query, "serviceName"))


def _to_uri(grpc: GrpcTransport) -> dict[str, str]:
    query_params = {}

    if grpc.service_name:
        query_params.update({"serviceName": grpc.service_name})

    return query_params
