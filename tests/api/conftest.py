import uuid

import pytest
from starlette.testclient import TestClient

from finalproject.api.api import RunFastAPIUsingTestClient
from finalproject.runner.setup import setup


@pytest.fixture
def http() -> TestClient:
    run_strategy = RunFastAPIUsingTestClient()
    test_database = f"test_{uuid.uuid4()}.db"
    setup(run_strategy=run_strategy, database=test_database).run_app()
    return run_strategy.client
