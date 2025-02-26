import pytest

from finalproject.models.models import Receipt, ReceiptItem
from finalproject.service.exceptions import (
    ProductNotFound,
    ReceiptItemNotFound,
    ReceiptNotFound,
    ShiftNotFound,
)
from finalproject.service.receipts import (
    ReceiptService,
)
from finalproject.store.paid_receipt import PaidReceiptStore


def test_should_add_and_get_empty_receipt(receipt_service: ReceiptService) -> None:
    receipt = Receipt(shift_id="1")
    receipt_response = receipt_service.add_receipt(receipt)
    assert receipt_response.compare_without_id(receipt)
    assert receipt_service.get_receipt(receipt_response.id).compare_without_id(receipt)


def test_should_add_receipt_with_items(receipt_service: ReceiptService) -> None:
    receipt = Receipt(
        items=[
            ReceiptItem(product_id="1", quantity=1, price=1.0),
            ReceiptItem(product_id="2", quantity=2, price=2.0),
        ],
        shift_id="1",
    )
    receipt_response = receipt_service.add_receipt(receipt)
    assert receipt_response.compare_without_id(receipt)
    assert receipt_service.get_receipt(receipt_response.id).compare_without_id(receipt)


def test_should_get_all_receipts(receipt_service: ReceiptService) -> None:
    assert len(receipt_service.get_all_receipts()) == 0

    receipt_1 = Receipt(shift_id="1")
    receipt_2 = Receipt(
        items=[
            ReceiptItem(product_id="1", quantity=1, price=1.0),
            ReceiptItem(product_id="2", quantity=2, price=2.0),
        ],
        shift_id="1",
    )
    receipt_service.add_receipt(receipt_1)
    receipt_service.add_receipt(receipt_2)

    all_receipts = receipt_service.get_all_receipts()

    assert len(all_receipts) == 2
    assert receipt_1.in_list_without_id(all_receipts)
    assert receipt_2.in_list_without_id(all_receipts)


def test_should_raise_receipt_not_found_when_getting_non_existent_receipt(
    receipt_service: ReceiptService,
) -> None:
    pytest.raises(ReceiptNotFound, receipt_service.get_receipt, "1")


def test_should_close_receipt(
    receipt_service: ReceiptService,
    paid_receipt_store: PaidReceiptStore,
) -> None:
    receipt = receipt_service.add_receipt(
        Receipt(
            items=[ReceiptItem(product_id="1", quantity=1, price=1.0)],
            shift_id="1",
        )
    )
    receipt_service.close_receipt(receipt.id, "GEL")

    receipt = receipt_service.get_receipt(receipt.id)
    assert not receipt.open
    assert paid_receipt_store.filter_by_field("receipt_id", receipt.id)[0].paid == 1.0


def test_raise_receipt_not_found_on_closing_non_existent_receipt(
    receipt_service: ReceiptService,
) -> None:
    receipt_service.add_receipt(Receipt(shift_id="1"))
    pytest.raises(ReceiptNotFound, receipt_service.close_receipt, "2", "")


def test_should_add_item_to_receipt(receipt_service: ReceiptService) -> None:
    receipt = receipt_service.add_receipt(
        Receipt(shift_id="1")
    )
    item = ReceiptItem(product_id="1", quantity=1, price=1.0)

    receipt = receipt_service.update_product_in_receipt(
        receipt_id=receipt.id, product_id=item.product_id, quantity=item.quantity
    )

    assert item.in_list_without_id(receipt.items)
    assert len(receipt.items) == 1


def test_should_raise_receipt_not_found_when_adding_item_to_non_existent_receipt(
    receipt_service: ReceiptService,
) -> None:
    item = ReceiptItem(product_id="1", quantity=1, price=1.0)
    pytest.raises(
        ReceiptNotFound,
        receipt_service.update_product_in_receipt,
        "1",
        item.product_id,
        item.quantity,
    )


def test_should_raise_product_not_found_when_adding_item_with_non_existent_product(
    receipt_service: ReceiptService,
) -> None:
    receipt = receipt_service.add_receipt(
        Receipt(shift_id="1")
    )

    item = ReceiptItem(product_id="3", quantity=1, price=1.0)
    pytest.raises(
        ProductNotFound,
        receipt_service.update_product_in_receipt,
        receipt.id,
        item.product_id,
        item.quantity,
    )


def test_should_update_item_in_receipt(receipt_service: ReceiptService) -> None:
    receipt = receipt_service.add_receipt(
        Receipt(
            items=[ReceiptItem(product_id="1", quantity=1, price=1.0)],
            shift_id="1",
        )
    )

    receipt_service.update_product_in_receipt(
        receipt_id=receipt.id,
        product_id=receipt.items[0].product_id,
        quantity=2,
    )

    compare_receipt = Receipt(
        items=[ReceiptItem(product_id="1", quantity=3, price=1.0)],
        shift_id="1",
    )

    assert receipt_service.get_receipt(receipt.id).compare_without_id_and_items_id(
        compare_receipt
    )


def test_should_remove_item_from_receipt(receipt_service: ReceiptService) -> None:
    receipt = receipt_service.add_receipt(
        Receipt(
            items=[ReceiptItem(product_id="1", quantity=1, price=1.0)],
            shift_id="1",
        )
    )

    receipt_service.remove_product_from_receipt(receipt.id, receipt.items[0].product_id)

    assert receipt_service.get_receipt(receipt.id).compare_without_id(
        Receipt(shift_id="1")
    )


def test_should_raise_receipt_item_not_found_when_removing_non_existent_item(
    receipt_service: ReceiptService,
) -> None:
    receipt = receipt_service.add_receipt(
        Receipt(shift_id="1")
    )
    pytest.raises(
        ReceiptItemNotFound,
        receipt_service.remove_product_from_receipt,
        receipt.id,
        "1",
    )


def test_should_get_receipts_by_shift_id(receipt_service: ReceiptService) -> None:
    receipt1 = Receipt(
        items=[ReceiptItem(product_id="1", quantity=1, price=1.0)],
        shift_id="1",
    )
    receipt2 = Receipt(shift_id="2")
    receipt_service.add_receipt(receipt1)

    assert len(receipt_service.get_receipts_by_shift_id("1")) == 1
    assert len(receipt_service.get_receipts_by_shift_id("2")) == 0

    receipt_service.add_receipt(receipt2)

    assert len(receipt_service.get_receipts_by_shift_id("1")) == 1
    assert len(receipt_service.get_receipts_by_shift_id("2")) == 1


def test_should_raise_shift_not_found_when_getting_receipts_by_non_existent_shift_id(
    receipt_service: ReceiptService,
) -> None:
    pytest.raises(ShiftNotFound, receipt_service.get_receipts_by_shift_id, "3")
