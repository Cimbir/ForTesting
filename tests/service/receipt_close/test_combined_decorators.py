from finalproject.models.campaigns import (
    BuyNGetN,
    Combo,
    ComboItem,
    ProductDiscount,
    ReceiptDiscount,
)
from finalproject.models.models import ReceiptItem
from finalproject.service.receipt_close.buy_n_get_n_decorator import BuyNGetNDecorator
from finalproject.service.receipt_close.combo_decorator import ComboDecorator
from finalproject.service.receipt_close.product_discount_decorator import (
    ProductDiscountDecorator,
)
from finalproject.service.receipt_close.receipt_close import ReceiptClose
from finalproject.service.receipt_close.receipt_discount_decorator import (
    ReceiptDiscountDecorator,
)
from tests.service.receipt_close.utils import get_receipt


def test_should_return_empty_result(def_rec_close: ReceiptClose) -> None:
    def_rec_close = ProductDiscountDecorator(
        def_rec_close, ProductDiscount(product_id="1", discount=0.1)
    )
    def_rec_close = ReceiptDiscountDecorator(
        def_rec_close, ReceiptDiscount(discount=0.1, minimum_total=100)
    )
    def_rec_close = ComboDecorator(def_rec_close, Combo(discount=0.1))
    def_rec_close = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            buy_product_id="1",
            buy_product_n=1,
            get_product_id="1",
            get_product_n=1,
        ),
    )

    result = def_rec_close.close(get_receipt([]))

    assert result.price == 0.0
    assert len(result.added_products) == 0


def test_should_discount_with_product_and_receipt(
    def_rec_close: ReceiptClose,
) -> None:
    def_rec_close = ReceiptDiscountDecorator(
        def_rec_close, ReceiptDiscount(discount=0.1, minimum_total=100)
    )
    def_rec_close = ProductDiscountDecorator(
        def_rec_close, ProductDiscount(product_id="1", discount=0.1)
    )

    result = def_rec_close.close(
        get_receipt(
            [
                ReceiptItem(product_id="1", quantity=20, price=10.0),
                ReceiptItem(product_id="2", quantity=1, price=10.0),
            ]
        )
    )

    assert result.price == (20 * 10.0 * 0.9 + 10.0) * 0.9


def test_should_discount_combo_part_with_products(
    def_rec_close: ReceiptClose,
) -> None:
    def_rec_close = ComboDecorator(
        def_rec_close,
        Combo(
            discount=0.1,
            items=[
                ComboItem(id="1", product_id="1", quantity=1),
                ComboItem(id="2", product_id="2", quantity=2),
            ],
        ),
    )
    def_rec_close = ProductDiscountDecorator(
        def_rec_close, ProductDiscount(product_id="1", discount=0.1)
    )

    result = def_rec_close.close(
        get_receipt(
            [
                ReceiptItem(product_id="1", quantity=3, price=7.0),
                ReceiptItem(product_id="2", quantity=4, price=8.0),
                ReceiptItem(product_id="3", quantity=1, price=10.0),
            ]
        )
    )

    assert result.price == 10.0 + 2 * (7.0 * 0.9 + 2 * 8.0) * 0.9 + 7.0 * 0.9


def test_should_not_change_price_with_added_items(
    def_rec_close: ReceiptClose,
) -> None:
    def_rec_close = ProductDiscountDecorator(
        def_rec_close, ProductDiscount(product_id="1", discount=0.1)
    )

    receipt = get_receipt(
        [
            ReceiptItem(product_id="1", quantity=10, price=10.0),
            ReceiptItem(product_id="2", quantity=1, price=10.0),
        ]
    )

    result = def_rec_close.close(receipt)

    assert result.price == 10.0 * 10 * 0.9 + 10.0
    assert len(result.added_products) == 0

    def_rec_close = BuyNGetNDecorator(
        def_rec_close,
        BuyNGetN(
            buy_product_id="1",
            buy_product_n=1,
            get_product_id="1",
            get_product_n=1,
        ),
    )

    result = def_rec_close.close(receipt)

    assert result.price == 10.0 * 10 * 0.9 + 10.0
    assert len(result.added_products) == 1
