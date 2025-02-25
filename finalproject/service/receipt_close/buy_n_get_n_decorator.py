from finalproject.models.campaigns import BuyNGetN
from finalproject.models.models import Receipt
from finalproject.service.receipt_close.receipt_close import (
    ReceiptClose,
    ReceiptCloseInfo,
    ReceiptCloseResult,
    get_info,
)
from finalproject.service.receipt_close.receipt_close_decorator import (
    ReceiptCloseDecorator,
)


class BuyNGetNDecorator(ReceiptCloseDecorator):
    _buy_n_get_n: BuyNGetN

    def __init__(self, receipt_close: ReceiptClose, buy_n_get_n: BuyNGetN) -> None:
        super().__init__(receipt_close)
        self._buy_n_get_n = buy_n_get_n

    def close(
        self, receipt: Receipt, info: ReceiptCloseInfo | None = None
    ) -> ReceiptCloseResult:
        _info = get_info(info)

        buy_n = 0
        for item in receipt.items:
            if item.product_id == self._buy_n_get_n.buy_product_id:
                buy_n += item.quantity

        amount = buy_n // self._buy_n_get_n.buy_product_n
        if amount > 0:
            _info.added_products[self._buy_n_get_n.get_product_id] += (
                self._buy_n_get_n.get_product_n * amount
            )

        return self._receipt_close.close(receipt, _info)
