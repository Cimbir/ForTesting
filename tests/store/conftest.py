import pytest

from finalproject.store.distributor import SQLiteStoreDistributor, StoreDistributor


@pytest.fixture
def distributor() -> StoreDistributor:
    return SQLiteStoreDistributor(":memory:")
