import pytest
from starlette.testclient import TestClient

from finalproject.runner.setup import setup


@pytest.fixture
def http() -> TestClient:
    return TestClient(setup())