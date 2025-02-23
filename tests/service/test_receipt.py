from finalproject.models.models import Receipt, ReceiptItem
from finalproject.service.receipts import ReceiptService


def test_should_add_empty_receipt(receipt_service: ReceiptService) -> None:
    receipt = Receipt(id="1", open=True, items=[], paid=0, shift_id="1")
    assert receipt_service.add_receipt(receipt=receipt)
    assert receipt_service.get_receipt(receipt_id="1") == receipt


def test_should_add_receipt_with_items(receipt_service: ReceiptService) -> None:
    status = receipt_service.add_receipt(
        Receipt(
            id="1",
            open=True,
            items=[
                ReceiptItem(id="1", product_id="1", quantity=1, price=1.0),
                ReceiptItem(id="2", product_id="2", quantity=2, price=2.0),
            ],
            paid=0,
            shift_id="1",
        )
    )
    assert status

    assert receipt_service.get_receipt("1") == Receipt(
        id="1",
        open=True,
        items=[
            ReceiptItem(id="1", product_id="1", quantity=1, price=1.0),
            ReceiptItem(id="2", product_id="2", quantity=2, price=2.0),
        ],
        paid=0,
        shift_id="1",
    )


def test_should_get_all_receipts(receipt_service: ReceiptService) -> None:
    assert len(receipt_service.get_all_receipts()) == 0

    receipt_1 = Receipt(id="1", open=True, items=[], paid=0, shift_id="1")
    receipt_2 = Receipt(
        id="2",
        open=True,
        items=[
            ReceiptItem(id="1", product_id="1", quantity=1, price=1.0),
            ReceiptItem(id="2", product_id="2", quantity=2, price=2.0),
        ],
        paid=0,
        shift_id="1",
    )
    receipt_service.add_receipt(receipt_1)
    receipt_service.add_receipt(receipt_2)

    assert len(receipt_service.get_all_receipts()) == 2
    assert receipt_1 in receipt_service.get_all_receipts()
    assert receipt_2 in receipt_service.get_all_receipts()


def test_should_return_none_when_getting_non_existent_receipt(
    receipt_service: ReceiptService,
) -> None:
    receipt_service.add_receipt(
        Receipt(id="1", open=True, items=[], paid=0, shift_id="1")
    )

    assert receipt_service.get_receipt("2") is None


def test_should_close_receipt(receipt_service: ReceiptService) -> None:
    receipt_service.add_receipt(
        Receipt(id="1", open=True, items=[], paid=0, shift_id="1")
    )
    receipt_service.close_receipt("1", 10)

    receipt = receipt_service.get_receipt("1")
    assert receipt is not None
    assert not receipt.open
    assert receipt.paid == 10


def test_return_false_on_closing_non_existent_receipt(
    receipt_service: ReceiptService,
) -> None:
    receipt_service.add_receipt(
        Receipt(id="1", open=True, items=[], paid=0, shift_id="1")
    )

    assert not receipt_service.close_receipt("2", 10)


def test_should_add_item_to_receipt(receipt_service: ReceiptService) -> None:
    receipt_service.add_receipt(
        Receipt(id="1", open=True, items=[], paid=0, shift_id="1")
    )

    receipt_service.add_item_to_receipt(
        receipt_id="1",
        item=ReceiptItem(id="1", product_id="1", quantity=1, price=1.0),
    )

    assert receipt_service.get_receipt("1") == Receipt(
        id="1",
        open=True,
        items=[ReceiptItem(id="1", product_id="1", quantity=1, price=1.0)],
        paid=0,
        shift_id="1",
    )


def test_should_return_false_when_adding_item_to_non_existent_receipt(
    receipt_service: ReceiptService,
) -> None:
    receipt_service.add_receipt(
        Receipt(id="1", open=True, items=[], paid=0, shift_id="1")
    )

    assert not receipt_service.add_item_to_receipt(
        "2", ReceiptItem(id="1", product_id="1", quantity=1, price=1.0)
    )


def test_should_update_item_in_receipt(receipt_service: ReceiptService) -> None:
    receipt_service.add_receipt(
        Receipt(
            id="1",
            open=True,
            items=[ReceiptItem(id="1", product_id="1", quantity=1, price=1.0)],
            paid=0,
            shift_id="1",
        )
    )

    receipt_service.update_item_in_receipt(
        receipt_id="1",
        item=ReceiptItem(id="1", product_id="1", quantity=2, price=1.0),
    )

    assert receipt_service.get_receipt("1") == Receipt(
        id="1",
        open=True,
        items=[ReceiptItem(id="1", product_id="1", quantity=2, price=1.0)],
        paid=0,
        shift_id="1",
    )


def test_should_return_false_when_updating_non_existent_item(
    receipt_service: ReceiptService,
) -> None:
    receipt_service.add_receipt(
        Receipt(id="1", open=True, items=[], paid=0, shift_id="1")
    )

    assert not receipt_service.update_item_in_receipt(
        "1",
        ReceiptItem(id="1", product_id="1", quantity=1, price=1.0),
    )


def test_should_remove_item_from_receipt(receipt_service: ReceiptService) -> None:
    receipt_service.add_receipt(
        Receipt(
            id="1",
            open=True,
            items=[ReceiptItem(id="1", product_id="1", quantity=1, price=1.0)],
            paid=0,
            shift_id="1",
        )
    )

    receipt_service.remove_item_from_receipt("1", "1")

    assert receipt_service.get_receipt("1") == Receipt(
        id="1",
        open=True,
        items=[],
        paid=0,
        shift_id="1",
    )


def test_should_return_false_when_removing_non_existent_item(
    receipt_service: ReceiptService,
) -> None:
    receipt_service.add_receipt(
        Receipt(id="1", open=True, items=[], paid=0, shift_id="1")
    )
    assert not receipt_service.remove_item_from_receipt("1", "1")


def test_should_get_receipts_by_shift_id(receipt_service: ReceiptService) -> None:
    receipt_service.add_receipt(
        Receipt(
            id="1",
            open=True,
            items=[ReceiptItem(id="1", product_id="1", quantity=1, price=1.0)],
            paid=0,
            shift_id="1",
        )
    )

    assert len(receipt_service.get_receipts_by_shift_id("1")) == 1
    assert len(receipt_service.get_receipts_by_shift_id("2")) == 0

    receipt_service.add_receipt(
        Receipt(
            id="2",
            open=True,
            items=[ReceiptItem(id="2", product_id="2", quantity=1, price=1.0)],
            paid=0,
            shift_id="2",
        )
    )

    assert len(receipt_service.get_receipts_by_shift_id("1")) == 1
    assert len(receipt_service.get_receipts_by_shift_id("2")) == 1
    assert len(receipt_service.get_receipts_by_shift_id("3")) == 0
