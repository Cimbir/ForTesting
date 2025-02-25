from finalproject.models.campaigns import ProductDiscount
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


class ProductDiscountDecorator(ReceiptCloseDecorator):
    _product_discount: ProductDiscount

    def __init__(
        self, receipt_close: ReceiptClose, product_discount: ProductDiscount
    ) -> None:
        super().__init__(receipt_close)
        self._product_discount = product_discount

    def close(
        self, receipt: Receipt, info: ReceiptCloseInfo | None = None
    ) -> ReceiptCloseResult:
        _info = get_info(info)

        _info.discounts[self._product_discount.product_id] *= (
            1 - self._product_discount.discount
        )

        return self._receipt_close.close(receipt, _info)
