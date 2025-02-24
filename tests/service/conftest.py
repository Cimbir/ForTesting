import pytest

from finalproject.service.campaigns import CampaignService
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


@pytest.fixture
def campaign_service(distributor: StoreDistributor) -> CampaignService:
    return CampaignService(
        distributor.products(),
        distributor.buy_n_get_n(),
        distributor.combos(),
        distributor.combo_items(),
        distributor.product_discount(),
        distributor.receipt_discounts(),
    )
