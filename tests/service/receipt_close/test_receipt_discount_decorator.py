from finalproject.models.campaigns import ReceiptDiscount
from finalproject.models.models import ReceiptItem
from finalproject.service.receipt_close.receipt_close import ReceiptClose
from finalproject.service.receipt_close.receipt_discount_decorator import (
    ReceiptDiscountDecorator,
)
from tests.service.receipt_close.utils import get_receipt


def test_should_return_zero_on_empty_receipt(
    def_rec_close: ReceiptClose,
) -> None:
    rec_discount = ReceiptDiscountDecorator(
        def_rec_close, ReceiptDiscount(discount=0.1, minimum_total=10.0)
    )
    assert rec_discount.close(get_receipt([])).price == 0.0


def test_should_discount_receipt(def_rec_close: ReceiptClose) -> None:
    rec_discount = ReceiptDiscountDecorator(
        def_rec_close, ReceiptDiscount(discount=0.1, minimum_total=10.0)
    )
    assert (
        rec_discount.close(
            get_receipt([ReceiptItem(product_id="1", quantity=1, price=10.0)])
        ).price
        == 9.0
    )


def test_should_not_discount_because_lower_than_main(
    def_rec_close: ReceiptClose,
) -> None:
    rec_discount = ReceiptDiscountDecorator(
        def_rec_close, ReceiptDiscount(discount=0.1, minimum_total=10.0)
    )
    assert (
        rec_discount.close(
            get_receipt([ReceiptItem(product_id="1", quantity=1, price=9.0)])
        ).price
        == 9.0
    )


def test_should_discount_multiple_products(def_rec_close: ReceiptClose) -> None:
    rec_discount = ReceiptDiscountDecorator(
        def_rec_close, ReceiptDiscount(discount=0.1, minimum_total=10.0)
    )
    assert (
        rec_discount.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=1, price=7.0),
                    ReceiptItem(product_id="2", quantity=1, price=12.0),
                ]
            )
        ).price
        == (7.0 + 12.0) * 0.9
    )


def test_should_not_discount_if_total_lower_than_main(
    def_rec_close: ReceiptClose,
) -> None:
    rec_discount = ReceiptDiscountDecorator(
        def_rec_close, ReceiptDiscount(discount=0.1, minimum_total=10.0)
    )
    assert (
        rec_discount.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=1, price=4.0),
                    ReceiptItem(product_id="2", quantity=1, price=5.0),
                ]
            )
        ).price
        == 9.0
    )


def test_should_choose_the_only_discount_that_fits(
    def_rec_close: ReceiptClose,
) -> None:
    rec_discount = ReceiptDiscountDecorator(
        def_rec_close, ReceiptDiscount(discount=0.1, minimum_total=10.0)
    )
    rec_discount = ReceiptDiscountDecorator(
        rec_discount, ReceiptDiscount(discount=0.2, minimum_total=20.0)
    )
    assert (
        rec_discount.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=1, price=3.0),
                    ReceiptItem(product_id="2", quantity=1, price=10.0),
                ]
            )
        ).price
        == (3.0 + 10.0) * 0.9
    )


def test_should_choose_the_best_discount(def_rec_close: ReceiptClose) -> None:
    rec_discount = ReceiptDiscountDecorator(
        def_rec_close, ReceiptDiscount(discount=0.1, minimum_total=10.0)
    )
    rec_discount = ReceiptDiscountDecorator(
        rec_discount, ReceiptDiscount(discount=0.2, minimum_total=20.0)
    )
    assert (
        rec_discount.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=1, price=13.0),
                    ReceiptItem(product_id="2", quantity=1, price=10.0),
                ]
            )
        ).price
        == (13.0 + 10.0) * 0.8
    )
