import pytest

from finalproject.models.campaigns import ReceiptDiscount
from finalproject.service.campaigns.receipt_discounts import ReceiptDiscountService
from finalproject.service.exceptions import ReceiptDiscountNotFound


def test_should_add_and_get_receipt_discount(receipt_discount_service: ReceiptDiscountService) -> None:
    receipt_discount = ReceiptDiscount(
        id="",
        minimum_total=10,
        discount=10,
    )
    receipt_discount_response = receipt_discount_service.add_receipt_discount(receipt_discount)
    assert receipt_discount_response.compare_without_id(receipt_discount)
    assert receipt_discount_service.get_receipt_discount(
        receipt_discount_response.id
    ).compare_without_id(receipt_discount)


def test_should_get_all_receipt_discounts(receipt_discount_service: ReceiptDiscountService) -> None:
    assert len(receipt_discount_service.get_all_receipt_discounts()) == 0

    receipt_discount_1 = ReceiptDiscount(
        id="1",
        minimum_total=10,
        discount=10,
    )
    receipt_discount_2 = ReceiptDiscount(
        id="2",
        minimum_total=10,
        discount=10,
    )
    receipt_discount_service.add_receipt_discount(receipt_discount_1)
    receipt_discount_service.add_receipt_discount(receipt_discount_2)

    assert len(receipt_discount_service.get_all_receipt_discounts()) == 2
    assert receipt_discount_service.get_all_receipt_discounts()[0].compare_without_id(
        receipt_discount_1
    )
    assert receipt_discount_service.get_all_receipt_discounts()[1].compare_without_id(
        receipt_discount_2
    )


def test_should_remove_receipt_discount(receipt_discount_service: ReceiptDiscountService) -> None:
    receipt_discount = ReceiptDiscount(
        id="",
        minimum_total=10,
        discount=10,
    )
    receipt_discount_response = receipt_discount_service.add_receipt_discount(receipt_discount)
    receipt_discount_service.remove_receipt_discount(receipt_discount_response.id)
    pytest.raises(
        ReceiptDiscountNotFound,
        receipt_discount_service.get_receipt_discount,
        receipt_discount_response.id,
    )


def test_should_not_remove_non_existent_receipt_discount(
    receipt_discount_service: ReceiptDiscountService,
) -> None:
    pytest.raises(
        ReceiptDiscountNotFound, receipt_discount_service.remove_receipt_discount, "1"
    )


def test_should_raise_receipt_discount_not_found_when_getting_non_existent_discount(
    receipt_discount_service: ReceiptDiscountService,
) -> None:
    pytest.raises(ReceiptDiscountNotFound, receipt_discount_service.get_receipt_discount, "1")
