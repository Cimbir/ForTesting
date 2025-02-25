from finalproject.models.campaigns import Combo, ComboItem
from finalproject.models.models import Receipt, ReceiptItem
from finalproject.service.receipt_close.receipt_close import (
    ReceiptClose,
    ReceiptCloseInfo,
    ReceiptCloseResult,
    get_info,
)
from finalproject.service.receipt_close.receipt_close_decorator import (
    ReceiptCloseDecorator,
)


class ComboDecorator(ReceiptCloseDecorator):
    _combo: Combo

    def __init__(self, receipt_close: ReceiptClose, combo: Combo) -> None:
        super().__init__(receipt_close)
        self._combo = combo

    def _get_left_for_combo(self, item: ReceiptItem, info: ReceiptCloseInfo) -> int:
        for combo_discount in info.combo_discounts[item.product_id]:
            return item.quantity - combo_discount[1]
        return item.quantity

    def _amount_satisfies_combo_item(
        self, combo_item: ComboItem, receipt: Receipt, info: ReceiptCloseInfo
    ) -> int:
        for item in receipt.items:
            if (
                item.product_id == combo_item.product_id
                and self._get_left_for_combo(item, info) >= combo_item.quantity
            ):
                return self._get_left_for_combo(item, info) // combo_item.quantity
        return 0

    def close(
        self, receipt: Receipt, info: ReceiptCloseInfo | None = None
    ) -> ReceiptCloseResult:
        _info = get_info(info)

        combo_satisfied_amount = float("inf")
        for combo_item in self._combo.items:
            combo_satisfied_amount = min(
                combo_satisfied_amount,
                self._amount_satisfies_combo_item(combo_item, receipt, _info),
            )

        if combo_satisfied_amount > 0:
            for combo_item in self._combo.items:
                _info.combo_discounts[combo_item.product_id].append(
                    (
                        1 - self._combo.discount,
                        combo_item.quantity * int(combo_satisfied_amount),
                    )
                )

        return self._receipt_close.close(receipt, _info)
