from finalproject.models.campaigns import ProductDiscount
from finalproject.models.models import ReceiptItem
from finalproject.service.receipt_close.product_discount_decorator import (
    ProductDiscountDecorator,
)
from finalproject.service.receipt_close.receipt_close import ReceiptClose
from tests.service.receipt_close.utils import get_receipt


def test_should_return_zero_when_no_items(def_rec_close: ReceiptClose) -> None:
    prod_discount = ProductDiscountDecorator(
        def_rec_close, ProductDiscount(product_id="1", discount=0.1)
    )
    assert prod_discount.close(get_receipt([])).price == 0.0


def test_should_discount_product(def_rec_close: ReceiptClose) -> None:
    prod_discount = ProductDiscountDecorator(
        def_rec_close, ProductDiscount(product_id="1", discount=0.1)
    )
    assert (
        prod_discount.close(
            get_receipt([ReceiptItem(product_id="1", quantity=1, price=1.0)])
        ).price
        == 0.9
    )
    assert (
        prod_discount.close(
            get_receipt([ReceiptItem(product_id="1", quantity=2, price=1.0)])
        ).price
        == 1.8
    )


def test_should_discount_one_in_multiple_products(
    def_rec_close: ReceiptClose,
) -> None:
    prod_discount = ProductDiscountDecorator(
        def_rec_close, ProductDiscount(product_id="2", discount=0.1)
    )
    assert (
        prod_discount.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=1, price=1.0),
                    ReceiptItem(product_id="2", quantity=1, price=2.0),
                ]
            )
        ).price
        == 1.0 + 1.8
    )


def test_should_not_discount_if_product_not_in_receipt(
    def_rec_close: ReceiptClose,
) -> None:
    prod_discount = ProductDiscountDecorator(
        def_rec_close, ProductDiscount(product_id="2", discount=0.1)
    )
    assert (
        prod_discount.close(
            get_receipt([ReceiptItem(product_id="1", quantity=1, price=1.0)])
        ).price
        == 1.0
    )


def test_should_discount_multiple_products(def_rec_close: ReceiptClose) -> None:
    prod_discount = ProductDiscountDecorator(
        def_rec_close, ProductDiscount(product_id="1", discount=0.1)
    )
    prod_discount = ProductDiscountDecorator(
        prod_discount, ProductDiscount(product_id="2", discount=0.2)
    )
    assert (
        prod_discount.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=1, price=1.0),
                    ReceiptItem(product_id="2", quantity=1, price=2.0),
                ]
            )
        ).price
        == 0.9 + 1.6
    )


def test_should_discount_same_product_multiple_times(
    def_rec_close: ReceiptClose,
) -> None:
    prod_discount = ProductDiscountDecorator(
        def_rec_close, ProductDiscount(product_id="1", discount=0.2)
    )
    prod_discount = ProductDiscountDecorator(
        prod_discount, ProductDiscount(product_id="1", discount=0.1)
    )
    assert (
        prod_discount.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=2, price=1.0),
                ]
            )
        ).price
        == 2 * 0.9 * 0.8
    )
