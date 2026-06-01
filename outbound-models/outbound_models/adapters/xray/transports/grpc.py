from outbound_models.models.transports.grpc import GrpcTransport
from outbound_models.schemas.xray.transports.grpc import GrpcTransportXray


def _from_xray(grpc: GrpcTransportXray) -> GrpcTransport:
    return GrpcTransport(
        service_name=grpc.service_name,
        idle_timeout=grpc.idle_timeout,
        ping_timeout=grpc.health_check_timeout,
        permit_without_stream=grpc.permit_without_stream,
    )
