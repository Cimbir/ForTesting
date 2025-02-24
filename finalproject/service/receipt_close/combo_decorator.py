from finalproject.models.campaigns import Combo, ComboItem
from finalproject.models.models import Receipt, ReceiptItem
from finalproject.service.receipt_close.receipt_close import (
    ReceiptClose,
    ReceiptCloseDecorator,
    ReceiptCloseInfo,
    default_info,
)


class ComboDecorator(ReceiptCloseDecorator):
    _combo: Combo

    def __init__(self, receipt_close: ReceiptClose, combo: Combo) -> None:
        super().__init__(receipt_close)
        self._combo = combo

    def _get_left_for_combo(self, item: ReceiptItem, info: ReceiptCloseInfo) -> int:
        left = item.quantity - info.free_items[item.product_id]
        for combo_discount in info.combo_discounts[item.product_id]:
            left -= combo_discount[1]
        return left

    def _satisfies_combo_item(
        self, combo_item: ComboItem, receipt: Receipt, info: ReceiptCloseInfo
    ) -> bool:
        combo_item_satisfied = False
        for item in receipt.items:
            if (
                item.product_id == combo_item.product_id
                and self._get_left_for_combo(item, info) >= combo_item.quantity
            ):
                combo_item_satisfied = True
                break
        return combo_item_satisfied

    def close(self, receipt: Receipt, info: ReceiptCloseInfo = default_info()) -> float:
        combo_satisfied = True
        for combo_item in self._combo.items:
            if not self._satisfies_combo_item(combo_item, receipt, info):
                combo_satisfied = False
                break

        if combo_satisfied:
            for combo_item in self._combo.items:
                info.combo_discounts[combo_item.product_id].append(
                    (self._combo.discount, combo_item.quantity)
                )

        return self._receipt_close.close(receipt, info)
