import pytest

from finalproject.store.distributor import StoreDistributor
from finalproject.store.receipt_discount import ReceiptDiscountRecord
from finalproject.store.store import RecordAlreadyExists, RecordNotFound


def test_should_add_and_get_receipt_discount_and(distributor: StoreDistributor) -> None:
    receipt_discount_store = distributor.receipt_discounts()

    receipt_discount = receipt_discount_store.add(
        ReceiptDiscountRecord("unique-id", 100, 0.1)
    )

    assert receipt_discount == receipt_discount_store.get_by_id("unique-id")


def test_should_list_all_receipt_discounts(distributor: StoreDistributor) -> None:
    receipt_discount_store = distributor.receipt_discounts()

    receipt_discount1 = receipt_discount_store.add(
        ReceiptDiscountRecord("unique-id-1", 100, 0.1)
    )
    receipt_discount2 = receipt_discount_store.add(
        ReceiptDiscountRecord("unique-id-2", 200, 0.2)
    )

    assert receipt_discount_store.list_all() == [receipt_discount1, receipt_discount2]


def test_should_remove_receipt_discounts_and_leave_others_untouched(
    distributor: StoreDistributor,
) -> None:
    receipt_discount_store = distributor.receipt_discounts()

    receipt_discount_store.add(ReceiptDiscountRecord("unique-id-1", 100, 0.1))
    receipt_discount2 = receipt_discount_store.add(
        ReceiptDiscountRecord("unique-id-2", 200, 0.2)
    )

    receipt_discount_store.remove("unique-id-1")

    assert receipt_discount_store.list_all() == [receipt_discount2]


def test_should_raise_error_when_adding_receipt_discount_with_same_id(
    distributor: StoreDistributor,
) -> None:
    receipt_discount_store = distributor.receipt_discounts()

    receipt_discount_store.add(ReceiptDiscountRecord("unique-id", 100, 0.1))

    pytest.raises(
        RecordAlreadyExists,
        receipt_discount_store.add,
        ReceiptDiscountRecord("unique-id", 100, 0.1),
    )


def test_should_raise_error_in_get_when_receipt_discount_does_not_exist(
    distributor: StoreDistributor,
) -> None:
    receipt_discount_store = distributor.receipt_discounts()

    pytest.raises(RecordNotFound, receipt_discount_store.get_by_id, "unique-id")


def test_should_raise_error_in_remove_when_receipt_discount_does_not_exist(
    distributor: StoreDistributor,
) -> None:
    receipt_discount_store = distributor.receipt_discounts()

    pytest.raises(RecordNotFound, receipt_discount_store.remove, "unique-id")
