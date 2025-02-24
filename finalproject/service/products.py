from typing import List

from finalproject.models.product import Product
from finalproject.service.exceptions import ProductNotFound
from finalproject.service.store_utils import generate_id
from finalproject.store.product import ProductStore
from finalproject.store.store import RecordNotFound


class ProductService:
    def __init__(self, product_store: ProductStore):
        self.product_store = product_store

    def add_product(self, product: Product) -> Product:
        product.id = generate_id()
        self.product_store.add(product.to_record())
        return product

    def get_product(self, product_id: str) -> Product:
        try:
            product_record = self.product_store.get_by_id(product_id)
        except RecordNotFound:
            raise ProductNotFound(product_id)
        return Product.from_record(product_record)

    def get_all_products(self) -> List[Product]:
        product_records = self.product_store.list_all()
        products = [Product.from_record(record) for record in product_records]
        return products

    def update_product(self, product: Product) -> Product:
        try:
            self.product_store.update(product.to_record())
        except RecordNotFound:
            raise ProductNotFound(product.id)
        return product

