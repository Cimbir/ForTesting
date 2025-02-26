from finalproject.models.campaigns import Combo, ComboItem
from finalproject.models.models import ReceiptItem
from finalproject.service.receipt_close.combo_decorator import ComboDecorator
from finalproject.service.receipt_close.receipt_close import ReceiptClose
from tests.service.receipt_close.utils import get_receipt


def test_should_return_zero_when_no_items(def_rec_close: ReceiptClose) -> None:
    combo = ComboDecorator(def_rec_close, Combo(discount=0.1))
    assert combo.close(get_receipt([])).price == 0.0


def test_should_discount_combo(def_rec_close: ReceiptClose) -> None:
    combo = ComboDecorator(
        def_rec_close,
        Combo(
            discount=0.1,
            items=[
                ComboItem(product_id="1", quantity=1),
            ],
        ),
    )

    assert (
        combo.close(
            get_receipt([ReceiptItem(product_id="1", quantity=1, price=1.0)])
        ).price
        == 0.9
    )


def test_should_not_discount_combo_when_not_enough_items(
    def_rec_close: ReceiptClose,
) -> None:
    combo = ComboDecorator(
        def_rec_close,
        Combo(
            discount=0.1,
            items=[
                ComboItem(product_id="1", quantity=2),
            ],
        ),
    )

    assert (
        combo.close(
            get_receipt([ReceiptItem(product_id="1", quantity=1, price=1.0)])
        ).price
        == 1.0
    )


def test_should_discount_combo_only_combo_item(
    def_rec_close: ReceiptClose,
) -> None:
    combo = ComboDecorator(
        def_rec_close,
        Combo(
            discount=0.1,
            items=[
                ComboItem(product_id="1", quantity=1),
            ],
        ),
    )

    assert (
        combo.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=1, price=1.0),
                    ReceiptItem(product_id="2", quantity=1, price=2.0),
                ]
            )
        ).price
        == 1.0 * 0.9 + 2.0
    )


def test_should_only_discount_combo_part_of_receipt_item(
    def_rec_close: ReceiptClose,
) -> None:
    combo = ComboDecorator(
        def_rec_close,
        Combo(
            discount=0.1,
            items=[
                ComboItem(product_id="1", quantity=2),
            ],
        ),
    )
    assert (
        combo.close(
            get_receipt([ReceiptItem(product_id="1", quantity=3, price=1.0)])
        ).price
        == 2.0 * 0.9 + 1.0
    )


def test_should_discount_multiple_same_combos(
    def_rec_close: ReceiptClose,
) -> None:
    combo = ComboDecorator(
        def_rec_close,
        Combo(
            discount=0.1,
            items=[
                ComboItem(product_id="1", quantity=2),
            ],
        ),
    )
    assert (
        combo.close(
            get_receipt([ReceiptItem(product_id="1", quantity=4, price=1.0)])
        ).price
        == 4.0 * 0.9
    )


def test_should_discount_combo_with_multiple_items(
    def_rec_close: ReceiptClose,
) -> None:
    combo = ComboDecorator(
        def_rec_close,
        Combo(
            discount=0.1,
            items=[
                ComboItem(product_id="1", quantity=1),
                ComboItem(product_id="2", quantity=1),
            ],
        ),
    )
    assert (
        combo.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=1, price=1.0),
                    ReceiptItem(product_id="2", quantity=1, price=2.0),
                    ReceiptItem(product_id="3", quantity=1, price=3.0),
                ]
            )
        ).price
        == (1.0 + 2.0) * 0.9 + 3.0
    )


def test_should_discount_with_multiple_different_combos(
    def_rec_close: ReceiptClose,
) -> None:
    combo = ComboDecorator(
        def_rec_close,
        Combo(
            discount=0.1,
            items=[
                ComboItem(product_id="1", quantity=1),
            ],
        ),
    )
    combo = ComboDecorator(
        combo,
        Combo(
            discount=0.2,
            items=[
                ComboItem(product_id="2", quantity=1),
            ],
        ),
    )
    assert (
        combo.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=1, price=1.0),
                    ReceiptItem(product_id="2", quantity=1, price=2.0),
                    ReceiptItem(product_id="3", quantity=1, price=3.0),
                ]
            )
        ).price
        == (1.0 * 0.9) + (2.0 * 0.8) + 3.0
    )


def test_should_only_discount_one_combo_because_overlapping_items(
    def_rec_close: ReceiptClose,
) -> None:
    combo = ComboDecorator(
        def_rec_close,
        Combo(
            discount=0.2,
            items=[
                ComboItem(product_id="1", quantity=1),
            ],
        ),
    )
    combo = ComboDecorator(
        combo,
        Combo(
            discount=0.1,
            items=[
                ComboItem(product_id="1", quantity=2),
            ],
        ),
    )
    assert (
        combo.close(
            get_receipt(
                [
                    ReceiptItem(product_id="1", quantity=2, price=1.0),
                    ReceiptItem(product_id="2", quantity=1, price=2.0),
                ]
            )
        ).price
        == (2.0 * 0.9) + 2.0
    )
