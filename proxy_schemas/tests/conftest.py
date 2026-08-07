import pytest
from proxy_schemas.adapters.adapter import OutboundAdapter


@pytest.fixture(scope="session")
def adapter() -> OutboundAdapter:
    return OutboundAdapter()
