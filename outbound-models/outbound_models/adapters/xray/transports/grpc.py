from typing import Any
from functools import partial

from outbound_models.models.transports.grpc import GrpcTransport

# from ..utils import _get_param


# def _from_xray(grpc_settings: dict[str, Any]) -> GrpcTransport:
#     get_param = partial(_get_param, grpc_settings)

#     return GrpcTransport(
#         service_name=get_param("service_name"),
#     )
