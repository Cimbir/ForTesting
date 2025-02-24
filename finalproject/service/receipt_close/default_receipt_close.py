from finalproject.models.models import Receipt
from finalproject.service.receipt_close.receipt_close import (
    ReceiptClose,
    ReceiptCloseInfo,
    calculate_cost,
    default_info,
)


class DefaultReceiptClose(ReceiptClose):
    def close(self, receipt: Receipt, info: ReceiptCloseInfo = default_info()) -> float:
        return calculate_cost(receipt, info)
