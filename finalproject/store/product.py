from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ProductRow:
    id: str
    name: str
    price: float
    shop_id: str
    is_removed: bool


class ProductStore(Protocol):
    def add_product(self, product: ProductRow) -> ProductRow:
        pass

    def get_product_by_id(self, product_id: str) -> ProductRow:
        pass

    def list_products(self) -> list[str]:
        pass

    def list_products_by_shop(self, shop_id: str) -> list[str]:
        pass

    def update_product(self, product: ProductRow) -> ProductRow:
        pass

    def remove_product(self, product_id: str) -> None:
        pass
