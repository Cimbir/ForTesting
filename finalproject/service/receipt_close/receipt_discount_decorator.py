from finalproject.models.campaigns import ReceiptDiscount
from finalproject.models.models import Receipt
from finalproject.service.receipt_close.receipt_close import (
    RECEIPT_KEY,
    ReceiptClose,
    ReceiptCloseInfo,
    calculate_cost, get_info,
)
from finalproject.service.receipt_close.receipt_close_decorator import ReceiptCloseDecorator


class ReceiptDiscountDecorator(ReceiptCloseDecorator):
    _receipt_discount: ReceiptDiscount

    def __init__(
        self, receipt_close: ReceiptClose, receipt_discount: ReceiptDiscount
    ) -> None:
        super().__init__(receipt_close)
        self._receipt_discount = receipt_discount

    def close(self, receipt: Receipt, info: ReceiptCloseInfo = None) -> float:
        info = get_info(info)

        current_total = calculate_cost(receipt, info)

        if current_total >= self._receipt_discount.minimum_total:
            info.discounts[RECEIPT_KEY] = min(
                info.discounts[RECEIPT_KEY],
                1 - self._receipt_discount.discount
            )

        return self._receipt_close.close(receipt, info)
