import pytest
from core.client import APIClient

@pytest.fixture
def api_client():
    return APIClient()