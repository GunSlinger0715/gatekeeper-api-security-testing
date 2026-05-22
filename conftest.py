import pytest
from core.client import APIClient

@pytest.fixture
def api_client():
    return APIClient()

from core.results import print_operational_summary

def pytest_sessionfinish(session, exitstatus):

    print_operational_summary()
    