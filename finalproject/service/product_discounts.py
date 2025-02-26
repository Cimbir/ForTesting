from dataclasses import dataclass

from finalproject.models.campaigns import ProductDiscount
from finalproject.service.exceptions import ProductDiscountNotFound
from finalproject.service.store_utils import _validate_product, generate_id
from finalproject.store.product import ProductStore
from finalproject.store.product_discount import ProductDiscountStore
from finalproject.store.store import RecordNotFound


@dataclass
class ProductDiscountService:
    product_store: ProductStore
    product_discount_store: ProductDiscountStore

    def add_product_discount(
        self, product_discount: ProductDiscount
    ) -> ProductDiscount:
        _validate_product(self.product_store, product_discount.product_id)
        product_discount.id = generate_id()
        self.product_discount_store.add(product_discount.to_record())
        return product_discount

    def get_product_discount(self, product_discount_id: str) -> ProductDiscount:
        try:
            product_discount_record = self.product_discount_store.get_by_id(
                product_discount_id
            )
            product_discount = ProductDiscount.from_record(product_discount_record)
            return product_discount
        except RecordNotFound:
            raise ProductDiscountNotFound(product_discount_id)

    def get_all_product_discounts(self) -> list[ProductDiscount]:
        product_discount_records = self.product_discount_store.list_all()
        product_discounts = [
            ProductDiscount.from_record(record) for record in product_discount_records
        ]
        return product_discounts

    def remove_product_discount(self, product_discount_id: str) -> None:
        try:
            self.product_discount_store.remove(product_discount_id)
        except RecordNotFound:
            raise ProductDiscountNotFound(product_discount_id)