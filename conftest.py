import pytest
from utils.api_client import APIClient

@pytest.fixture
def api_client():
    return APIClient()