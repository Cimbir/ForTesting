from finalproject.models.models import Receipt, ReceiptItem
from finalproject.service.receipt_close.default_receipt_close import DefaultReceiptClose
from tests.service.receipt_close.utils import get_receipt


def test_should_return_zero_when_no_items_in_receipt(def_rec_close: DefaultReceiptClose) -> None:
    assert def_rec_close.close(receipt=get_receipt([])) == 0.0

def test_should_return_sum_of_item_costs(def_rec_close: DefaultReceiptClose) -> None:
    receipt = get_receipt([
        ReceiptItem(
            id="1",
            product_id="1",
            quantity=1,
            price=1.0
        ),
        ReceiptItem(
            id="2",
            product_id="2",
            quantity=1,
            price=2.0
        ),
        ReceiptItem(
            id="3",
            product_id="3",
            quantity=1,
            price=3.0
        )
    ])
    assert def_rec_close.close(receipt=receipt) == 1.0 + 2.0 + 3.0

def test_should_return_sum_of_item_costs_with_multiple_quantities(def_rec_close: DefaultReceiptClose) -> None:
    receipt = get_receipt([
        ReceiptItem(
            id="1",
            product_id="1",
            quantity=2,
            price=1.0
        ),
        ReceiptItem(
            id="2",
            product_id="2",
            quantity=3,
            price=2.0
        ),
        ReceiptItem(
            id="3",
            product_id="3",
            quantity=4,
            price=3.0
        )
    ])
    assert def_rec_close.close(receipt=receipt) == 2 * 1.0 + 3 * 2.0 + 4 * 3.0

def test_should_handle_multiple_calls(def_rec_close: DefaultReceiptClose) -> None:
    assert def_rec_close.close(receipt=get_receipt([])) == 0.0
    assert def_rec_close.close(receipt=get_receipt([])) == 0.0
    assert def_rec_close.close(receipt=get_receipt([
        ReceiptItem(
            id="1",
            product_id="1",
            quantity=1,
            price=1.0
        )
    ])) == 1.0
    assert def_rec_close.close(receipt=get_receipt([
        ReceiptItem(
            id="1",
            product_id="1",
            quantity=1,
            price=1.0
        )
    ])) == 1.0