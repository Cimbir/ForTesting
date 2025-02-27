import pytest

from finalproject.store.distributor import StoreDistributor
from finalproject.store.paid_receipt import PaidReceiptRecord
from finalproject.store.store import RecordNotFound


def test_should_raise_not_found_error_when_receipt_not_paid(
    distributor: StoreDistributor,
) -> None:
    paid_receipt_store = distributor.paid_receipts()
    pytest.raises(RecordNotFound, paid_receipt_store.get_by_id, "unique-id-1")


def test_should_add_and_list_multiple_paid_receipts(
    distributor: StoreDistributor,
) -> None:
    paid_receipt_store = distributor.paid_receipts()

    paid_receipt1 = PaidReceiptRecord(
        id="unique-id-1", receipt_id="receipt-id-1", currency_name="USD", paid=9.99
    )
    paid_receipt_store.add(paid_receipt1)

    paid_receipt2 = PaidReceiptRecord(
        id="unique-id-2", receipt_id="receipt-id-2", currency_name="EUR", paid=99.99
    )
    paid_receipt_store.add(paid_receipt2)

    assert len(paid_receipt_store.list_all()) == 2
    assert paid_receipt1 in paid_receipt_store.list_all()
    assert paid_receipt2 in paid_receipt_store.list_all()
    assert paid_receipt_store.get_by_id("unique-id-1") == paid_receipt1
    assert paid_receipt_store.get_by_id("unique-id-2") == paid_receipt2
