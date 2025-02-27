from dataclasses import dataclass

from finalproject.models.models import Model
from finalproject.store.product import ProductRecord


@dataclass
class Product(Model):
    id: str = ""
    name: str = ""
    price: float = 0.0

    def to_record(self) -> ProductRecord:
        return ProductRecord(
            id=self.id,
            name=self.name,
            price=self.price,
        )

    @classmethod
    def from_record(cls, record: ProductRecord) -> "Product":
        return cls(
            id=record.id,
            name=record.name,
            price=record.price,
        )
