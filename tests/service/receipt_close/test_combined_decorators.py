from finalproject.models.campaigns import ProductDiscount, ReceiptDiscount, Combo, BuyNGetN
from finalproject.models.models import ReceiptItem
from finalproject.service.receipt_close.buy_n_get_n_decorator import BuyNGetNDecorator
from finalproject.service.receipt_close.combo_decorator import ComboDecorator
from finalproject.service.receipt_close.default_receipt_close import DefaultReceiptClose
from finalproject.service.receipt_close.product_discount_decorator import ProductDiscountDecorator
from finalproject.service.receipt_close.receipt_discount_decorator import ReceiptDiscountDecorator
from tests.service.receipt_close.utils import get_receipt


def test_should_return_empty_result(def_rec_close: DefaultReceiptClose) -> None:
    def_rec_close = ProductDiscountDecorator(def_rec_close, ProductDiscount(
        id="1",
        product_id="1",
        discount=0.1
    ))
    def_rec_close = ReceiptDiscountDecorator(def_rec_close, ReceiptDiscount(
        id="1",
        discount=0.1,
        minimum_total=100
    ))
    def_rec_close = ComboDecorator(def_rec_close, Combo(
        id="1",
        discount=0.1,
        name="test",
        items=[]
    ))
    def_rec_close = BuyNGetNDecorator(def_rec_close, BuyNGetN(
        id="1",
        buy_product_id="1",
        buy_product_n=1,
        get_product_id="1",
        get_product_n=1
    ))

    result = def_rec_close.close(get_receipt([]))

    assert result.price == 0.0
    assert len(result.added_products) == 0
