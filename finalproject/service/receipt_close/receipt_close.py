from dataclasses import dataclass
from typing import Protocol

from mypy.memprofile import defaultdict

from finalproject.models.models import Receipt

RECEIPT_KEY = "receipt"


@dataclass
class ReceiptCloseInfo:
    discounts: defaultdict[str, float]
    added_products: defaultdict[str, int]
    combo_discounts: defaultdict[str, list[tuple[float, int]]]

@dataclass
class ReceiptCloseResult:
    price: float
    added_products: defaultdict[str, int]

def get_info(info: ReceiptCloseInfo) -> ReceiptCloseInfo:
    if info is None:
        return ReceiptCloseInfo(
            defaultdict(lambda: 1.0), defaultdict(lambda: 0), defaultdict(lambda: [])
        )
    return info


def calculate_cost(receipt: Receipt, info: ReceiptCloseInfo) -> float:
    total = 0
    for item in receipt.items:
        paid_amount = item.quantity
        fit_combos = info.combo_discounts[item.product_id]

        item_cost = 0
        for combo in fit_combos:
            item_cost += combo[0] * combo[1]
            paid_amount -= combo[1]
        item_cost += paid_amount

        item_cost *= info.discounts[item.product_id] * item.price
        total += item_cost
    total *= info.discounts[RECEIPT_KEY]
    return total


class ReceiptClose(Protocol):
    def close(self, receipt: Receipt, info: ReceiptCloseInfo = None) -> ReceiptCloseResult:
        pass
