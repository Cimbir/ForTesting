import uuid

import pytest
from starlette.testclient import TestClient

from finalproject.api.api import RunFastAPIUsingTestClient
from finalproject.runner.setup import mock_setup
from finalproject.store.distributor import SQLiteStoreDistributor, StoreDistributor
from finalproject.store.product import ProductRecord
from finalproject.store.shift import ShiftRecord


@pytest.fixture
def distributor() -> StoreDistributor:
    distr = SQLiteStoreDistributor(f"test_{uuid.uuid4()}.db")
    distr.shifts().add(
        ShiftRecord(
            id="1",
            status="open",
            start_time="2021-01-01T00:00:00",
            end_time="2021-01-01T00:00:00",
        )
    )
    distr.products().add(
        ProductRecord(
            id="1",
            name="product",
            price=1.0,
        )
    )
    distr.products().add(
        ProductRecord(
            id="2",
            name="product2",
            price=2.0,
        )
    )
    return distr


@pytest.fixture
def http(distributor: StoreDistributor) -> TestClient:
    run_strategy = RunFastAPIUsingTestClient()
    mock_setup(run_strategy=run_strategy, distributor=distributor).run_app()
    return run_strategy.client
