from finalproject.models.models import ReceiptItem
from finalproject.service.receipt_close.receipt_close import ReceiptClose
from tests.service.receipt_close.utils import get_receipt


def test_should_return_zero_when_no_items_in_receipt(
    def_rec_close: ReceiptClose,
) -> None:
    assert def_rec_close.close(receipt=get_receipt([])).price == 0.0


def test_should_return_sum_of_item_costs(def_rec_close: ReceiptClose) -> None:
    receipt = get_receipt(
        [
            ReceiptItem(product_id="1", quantity=1, price=1.0),
            ReceiptItem(product_id="2", quantity=1, price=2.0),
            ReceiptItem(product_id="3", quantity=1, price=3.0),
        ]
    )
    assert def_rec_close.close(receipt=receipt).price == 1.0 + 2.0 + 3.0


def test_should_return_sum_of_item_costs_with_multiple_quantities(
    def_rec_close: ReceiptClose,
) -> None:
    receipt = get_receipt(
        [
            ReceiptItem(product_id="1", quantity=2, price=1.0),
            ReceiptItem(product_id="2", quantity=3, price=2.0),
            ReceiptItem(product_id="3", quantity=4, price=3.0),
        ]
    )
    assert def_rec_close.close(receipt=receipt).price == 2 * 1.0 + 3 * 2.0 + 4 * 3.0


def test_should_handle_multiple_calls(def_rec_close: ReceiptClose) -> None:
    assert def_rec_close.close(receipt=get_receipt([])).price == 0.0
    assert def_rec_close.close(receipt=get_receipt([])).price == 0.0
    assert (
        def_rec_close.close(
            receipt=get_receipt([ReceiptItem(product_id="1", quantity=1, price=1.0)])
        ).price
        == 1.0
    )
    assert (
        def_rec_close.close(
            receipt=get_receipt([ReceiptItem(product_id="1", quantity=1, price=1.0)])
        ).price
        == 1.0
    )
