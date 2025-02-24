from uuid import uuid4

from finalproject.models.campaigns import BuyNGetN
from finalproject.models.models import Receipt, ReceiptItem
from finalproject.models.product import Product
from finalproject.service.receipt_close.receipt_close import (
    ReceiptClose,
    ReceiptCloseInfo, get_info,
)
from finalproject.service.receipt_close.receipt_close_decorator import ReceiptCloseDecorator


class BuyNGetNDecorator(ReceiptCloseDecorator):
    _buy_n_get_n: BuyNGetN
    _product: Product

    def __init__(
        self, receipt_close: ReceiptClose, buy_n_get_n: BuyNGetN, product: Product
    ) -> None:
        super().__init__(receipt_close)
        self._buy_n_get_n = buy_n_get_n
        self._product = product

    def close(self, receipt: Receipt, info: ReceiptCloseInfo = None) -> float:
        info = get_info(info)

        buy_n = 0
        for item in receipt.items:
            if item.product_id == self._buy_n_get_n.buy_product_id:
                buy_n += item.quantity

        if buy_n >= self._buy_n_get_n.buy_product_n:
            gotten = False
            for item in receipt.items:
                if item.product_id == self._buy_n_get_n.get_product_id:
                    item.quantity += self._buy_n_get_n.get_product_n
                    gotten = True
                    break
            if not gotten:
                receipt.items.append(
                    ReceiptItem(
                        id=str(uuid4()),
                        product_id=self._buy_n_get_n.get_product_id,
                        quantity=self._buy_n_get_n.get_product_n,
                        price=self._product.price,
                    )
                )
            info.free_items[self._buy_n_get_n.get_product_id] += (
                self._buy_n_get_n.get_product_n
            )

        return self._receipt_close.close(receipt, info)
