import pytest
from starlette.testclient import TestClient

from finalproject.api.api import RunFastAPIUsingTestClient
from finalproject.runner.setup import setup


@pytest.fixture
def http() -> TestClient:
    run_strategy = RunFastAPIUsingTestClient()
    setup(run_strategy).run_app()
    return run_strategy.client
