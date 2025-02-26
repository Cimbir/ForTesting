from dataclasses import dataclass, field
from email.policy import default
from typing import Protocol, Sequence

from finalproject.store.receipt import ReceiptRecord
from finalproject.store.receipt_item import ReceiptItemRecord


class Model(Protocol):
    id: str = ""

    def compare_without_id(self, other: "Model") -> bool:
        without_id = {k: v for k, v in self.__dict__.items() if k != "id"}
        other_without_id = {k: v for k, v in other.__dict__.items() if k != "id"}
        return without_id == other_without_id

    def in_list_without_id(self, others: Sequence["Model"]) -> bool:
        return any(self.compare_without_id(other) for other in others)


@dataclass
class ReceiptItem(Model):
    id: str = ""
    product_id: str = ""
    quantity: int = 0.0
    price: float = 0.0

    def to_record(self, receipt_id: str) -> ReceiptItemRecord:
        return ReceiptItemRecord(
            id=self.id,
            receipt_id=receipt_id,
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


@dataclass
class Receipt(Model):
    id: str = ""
    open: bool = True
    shift_id: str = ""
    items: list[ReceiptItem] = field(default_factory=list)

    def to_record(self) -> ReceiptRecord:
        return ReceiptRecord(
            id=self.id,
            open=self.open,
            shift_id=self.shift_id,
        )

    @classmethod
    def from_record(cls, record: ReceiptRecord, items: list[ReceiptItem]) -> "Receipt":
        return cls(
            id=record.id,
            open=record.open,
            shift_id=record.shift_id,
            items=items,
        )

    def compare_without_id_and_items_id(self, other: "Receipt") -> bool:
        items_are_same = all(
            self_item.compare_without_id(other_item)
            for self_item, other_item in zip(self.items, other.items)
        )
        without_list = {
            k: v for k, v in self.__dict__.items() if k not in ["id", "items"]
        }
        other_without_list = {
            k: v for k, v in other.__dict__.items() if k not in ["id", "items"]
        }
        return without_list == other_without_list and items_are_same
