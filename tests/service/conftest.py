import pytest

from finalproject.service.receipts import ReceiptService
from finalproject.store.distributor import SQLiteStoreDistributor, StoreDistributor


@pytest.fixture
def distributor() -> StoreDistributor:
    return SQLiteStoreDistributor(":memory:")


@pytest.fixture
def receipt_service(distributor: StoreDistributor) -> ReceiptService:
    return ReceiptService(
        distributor.receipt(),
        distributor.receipt_items(),
        distributor.shifts(),
        distributor.products(),
    )
