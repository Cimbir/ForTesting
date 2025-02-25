from finalproject.models.models import Receipt
from finalproject.service.receipt_close.receipt_close import (
    ReceiptClose,
    ReceiptCloseInfo,
    calculate_cost,
    get_info, ReceiptCloseResult
)


class DefaultReceiptClose(ReceiptClose):
    def close(self, receipt: Receipt, info: ReceiptCloseInfo = None) -> ReceiptCloseResult:
        info = get_info(info)
        return ReceiptCloseResult(price=calculate_cost(receipt, info), added_products=info.added_products)
