from finalproject.models.models import Receipt
from finalproject.service.receipt_close.receipt_close import (
    ReceiptClose,
    ReceiptCloseInfo,
    ReceiptCloseResult,
    get_info,
)


class ReceiptCloseDecorator(ReceiptClose):
    _receipt_close: ReceiptClose

    def __init__(self, receipt_close: ReceiptClose) -> None:
        self._receipt_close = receipt_close

    def close(
        self, receipt: Receipt, info: ReceiptCloseInfo | None = None
    ) -> ReceiptCloseResult:
        _info = get_info(info)
        return self._receipt_close.close(receipt, _info)
