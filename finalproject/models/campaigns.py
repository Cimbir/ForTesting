from dataclasses import dataclass

from finalproject.models.models import Model
from finalproject.store.buy_n_get_n import BuyNGetNRecord
from finalproject.store.combo import ComboRecord
from finalproject.store.combo_item import ComboItemRecord
from finalproject.store.product_discount import ProductDiscountRecord
from finalproject.store.receipt_discount import ReceiptDiscountRecord


@dataclass
class BuyNGetN(Model):
    id: str
    buy_product_id: str
    buy_product_n: int
    get_product_id: str
    get_product_n: int

    def to_record(self) -> BuyNGetNRecord:
        return BuyNGetNRecord(
            id=self.id,
            buy_product_id=self.buy_product_id,
            buy_product_n=self.buy_product_n,
            get_product_id=self.get_product_id,
            get_product_n=self.get_product_n,
        )

    @classmethod
    def from_record(cls, record: BuyNGetNRecord) -> "BuyNGetN":
        return cls(
            id=record.id,
            buy_product_id=record.buy_product_id,
            buy_product_n=record.buy_product_n,
            get_product_id=record.get_product_id,
            get_product_n=record.get_product_n,
        )


@dataclass
class ProductDiscount(Model):
    id: str
    product_id: str
    discount: float

    def to_record(self) -> ProductDiscountRecord:
        return ProductDiscountRecord(
            id=self.id,
            product_id=self.product_id,
            discount=self.discount,
        )

    @classmethod
    def from_record(cls, record: ProductDiscountRecord) -> "ProductDiscount":
        return cls(
            id=record.id,
            product_id=record.product_id,
            discount=record.discount,
        )


@dataclass
class ReceiptDiscount(Model):
    id: str
    minimum_total: float
    discount: float

    def to_record(self) -> ReceiptDiscountRecord:
        return ReceiptDiscountRecord(
            id=self.id,
            minimum_total=self.minimum_total,
            discount=self.discount,
        )

    @classmethod
    def from_record(cls, record: ReceiptDiscountRecord) -> "ReceiptDiscount":
        return cls(
            id=record.id,
            minimum_total=record.minimum_total,
            discount=record.discount,
        )


@dataclass
class ComboItem(Model):
    id: str
    product_id: str
    quantity: int

    def to_record(self) -> ComboItemRecord:
        return ComboItemRecord(
            id=self.id,
            product_id=self.product_id,
            quantity=self.quantity,
        )

    @classmethod
    def from_record(cls, record: ComboItemRecord) -> "ComboItem":
        return cls(
            id=record.id,
            product_id=record.product_id,
            quantity=record.quantity,
        )


@dataclass
class Combo(Model):
    id: str
    name: str
    discount: float
    items: list[ComboItem]

    def to_record(self) -> ComboRecord:
        return ComboRecord(
            id=self.id,
            name=self.name,
            discount=self.discount,
        )

    @classmethod
    def from_record(cls, record: ComboRecord, items: list[ComboItem]) -> "Combo":
        return cls(
            id=record.id,
            name=record.name,
            discount=record.discount,
            items=items,
        )
