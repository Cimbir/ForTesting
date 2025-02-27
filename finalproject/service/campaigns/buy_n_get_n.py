from dataclasses import dataclass

from finalproject.models.campaigns import BuyNGetN
from finalproject.service.exceptions import BuyNGetNNotFound
from finalproject.service.store_utils import _validate_product, generate_id
from finalproject.store.buy_n_get_n import BuyNGetNStore
from finalproject.store.product import ProductStore
from finalproject.store.store import RecordNotFound


@dataclass
class BuyNGetNService:
    product_store: ProductStore
    buy_n_get_n_store: BuyNGetNStore

    def add_buy_n_get_n(self, buy_n_get_n: BuyNGetN) -> BuyNGetN:
        _validate_product(self.product_store, buy_n_get_n.buy_product_id)
        _validate_product(self.product_store, buy_n_get_n.get_product_id)
        buy_n_get_n.id = generate_id()
        self.buy_n_get_n_store.add(buy_n_get_n.to_record())
        return buy_n_get_n

    def get_buy_n_get_n(self, buy_n_get_n_id: str) -> BuyNGetN:
        try:
            buy_n_get_n_record = self.buy_n_get_n_store.get_by_id(buy_n_get_n_id)
            buy_n_get_n = BuyNGetN.from_record(buy_n_get_n_record)
            return buy_n_get_n
        except RecordNotFound:
            raise BuyNGetNNotFound(buy_n_get_n_id)

    def get_all_buy_n_get_ns(self) -> list[BuyNGetN]:
        buy_n_get_n_records = self.buy_n_get_n_store.list_all()
        buy_n_get_ns = [BuyNGetN.from_record(record) for record in buy_n_get_n_records]
        return buy_n_get_ns

    def remove_buy_n_get_n(self, buy_n_get_n_id: str) -> None:
        try:
            self.buy_n_get_n_store.remove(buy_n_get_n_id)
        except RecordNotFound:
            raise BuyNGetNNotFound(buy_n_get_n_id)
