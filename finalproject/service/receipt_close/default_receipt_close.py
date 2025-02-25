from finalproject.models.models import Receipt
from finalproject.service.receipt_close.receipt_close import (
    ReceiptClose,
    ReceiptCloseInfo,
    ReceiptCloseResult,
    calculate_cost,
    get_info,
)


class DefaultReceiptClose(ReceiptClose):
    def close(
        self, receipt: Receipt, info: ReceiptCloseInfo | None = None
    ) -> ReceiptCloseResult:
        _info = get_info(info)
        return ReceiptCloseResult(
            price=calculate_cost(receipt, _info), added_products=_info.added_products
        )
