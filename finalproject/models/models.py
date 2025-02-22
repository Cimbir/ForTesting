from dataclasses import dataclass
from typing import Protocol

from finalproject.store.receipt import ReceiptRecord
from finalproject.store.receipt_items import ReceiptItemRecord


class Model(Protocol):
    id: str


@dataclass(frozen=True)
class ReceiptItem(Model):
    id: str
    product_id: str
    quantity: int
    price: float


    def to_record(self) -> ReceiptItemRecord:
        return ReceiptItemRecord(
            id=self.id,
            product_id=self.product_id,
            quantity=self.quantity,
            price=self.price,
        )

    @classmethod
    def from_record(cls, record: ReceiptItemRecord) -> "ReceiptItem":
        return cls(
            id=record.id,
            product_id=record.product_id,
            quantity=record.quantity,
            price=record.price,
        )

@dataclass(frozen=True)
class Receipt(Model):
    id: str
    open: bool
    paid: float
    shift_id: str
    items: list[ReceiptItem]

    def to_record(self) -> ReceiptRecord:
        return ReceiptRecord(
            id=self.id,
            open=self.open,
            paid=self.paid,
            shift_id=self.shift_id,
        )

    @classmethod
    def from_record(cls, record: ReceiptRecord, items: list[ReceiptItem]) -> "Receipt":
        return cls(
            id=record.id,
            open=record.open,
            paid=record.paid,
            shift_id=record.shift_id,
            items=items,
        )

