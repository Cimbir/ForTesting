import pytest

from finalproject.service.campaigns.buy_n_get_n import BuyNGetNService
from finalproject.service.campaigns.combos import ComboService
from finalproject.service.campaigns.product_discounts import ProductDiscountService
from finalproject.service.campaigns.receipt_discounts import ReceiptDiscountService
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
def combo_service(distributor: StoreDistributor) -> ComboService:
    return ComboService(
        distributor.products(),
        distributor.combos(),
        distributor.combo_items(),
    )


@pytest.fixture
def product_discount_service(distributor: StoreDistributor) -> ProductDiscountService:
    return ProductDiscountService(
        distributor.products(),
        distributor.product_discount(),
    )


@pytest.fixture
def receipt_discount_service(distributor: StoreDistributor) -> ReceiptDiscountService:
    return ReceiptDiscountService(
        distributor.receipt_discounts(),
    )


@pytest.fixture
def buy_n_get_n_service(distributor: StoreDistributor) -> BuyNGetNService:
    return BuyNGetNService(
        distributor.products(),
        distributor.buy_n_get_n(),
    )
