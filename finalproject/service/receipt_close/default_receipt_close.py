from finalproject.models.models import Receipt
from finalproject.service.receipt_close.receipt_close import (
    ReceiptClose,
    ReceiptCloseInfo,
    calculate_cost,
    get_info
)


class DefaultReceiptClose(ReceiptClose):
    def close(self, receipt: Receipt, info: ReceiptCloseInfo = None) -> float:
        info = get_info(info)
        return calculate_cost(receipt, info)