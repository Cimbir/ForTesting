import pytest

from finalproject.service.campaigns import CampaignService
from finalproject.service.currency_conversion.exchangerate_api_adapter import (
    ExchangeRateAPIFacade,
)
from finalproject.service.receipts import ReceiptService
from finalproject.store.buy_n_get_n import BuyNGetNStore
from finalproject.store.combo import ComboStore
from finalproject.store.combo_item import ComboItemStore
from finalproject.store.distributor import SQLiteStoreDistributor, StoreDistributor
from finalproject.store.paid_receipt import PaidReceiptStore
from finalproject.store.product import ProductRecord, ProductStore
from finalproject.store.product_discount import ProductDiscountStore
from finalproject.store.receipt import ReceiptStore
from finalproject.store.receipt_discount import ReceiptDiscountStore
from finalproject.store.receipt_item import ReceiptItemStore
from finalproject.store.shift import ShiftRecord, ShiftStore


@pytest.fixture
def distributor() -> StoreDistributor:
    return SQLiteStoreDistributor(":memory:")


@pytest.fixture
def receipt_store(distributor: StoreDistributor) -> ReceiptStore:
    return distributor.receipt()


@pytest.fixture
def receipt_item_store(distributor: StoreDistributor) -> ReceiptItemStore:
    return distributor.receipt_items()


@pytest.fixture
def shift_store(distributor: StoreDistributor) -> ShiftStore:
    return distributor.shifts()


@pytest.fixture
def product_store(distributor: StoreDistributor) -> ProductStore:
    return distributor.products()


@pytest.fixture
def paid_receipt_store(distributor: StoreDistributor) -> PaidReceiptStore:
    return distributor.paid_receipts()


@pytest.fixture
def combo_store(distributor: StoreDistributor) -> ComboStore:
    return distributor.combos()


@pytest.fixture
def combo_item_store(distributor: StoreDistributor) -> ComboItemStore:
    return distributor.combo_items()


@pytest.fixture
def product_discount_store(distributor: StoreDistributor) -> ProductDiscountStore:
    return distributor.product_discount()


@pytest.fixture
def receipt_discount_store(distributor: StoreDistributor) -> ReceiptDiscountStore:
    return distributor.receipt_discounts()


@pytest.fixture
def buy_n_get_n_store(distributor: StoreDistributor) -> BuyNGetNStore:
    return distributor.buy_n_get_n()


@pytest.fixture
def receipt_service(distributor: StoreDistributor) -> ReceiptService:
    distributor.shifts().add(ShiftRecord("1", "open", "2021-01-01", "2021-01-02"))
    distributor.shifts().add(ShiftRecord("2", "open", "2021-01-01", "2021-01-02"))
    distributor.products().add(ProductRecord("1", "product 1", 1.0))
    distributor.products().add(ProductRecord("2", "product 2", 2.0))
    return ReceiptService(
        distributor.receipt(),
        distributor.receipt_items(),
        distributor.shifts(),
        distributor.products(),
        distributor.paid_receipts(),
        distributor.combos(),
        distributor.combo_items(),
        distributor.product_discount(),
        distributor.receipt_discounts(),
        distributor.buy_n_get_n(),
        ExchangeRateAPIFacade(),
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
