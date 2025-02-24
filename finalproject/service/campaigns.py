from finalproject.models.campaigns import (
    BuyNGetN,
    Combo,
    ComboItem,
    ProductDiscount,
    ReceiptDiscount,
)
from finalproject.service.exceptions import (
    BuyNGetNNotFound,
    ComboNotFound,
    ProductDiscountNotFound,
    ProductNotFound,
    ReceiptDiscountNotFound,
)
from finalproject.store.buy_n_get_n import BuyNGetNStore
from finalproject.store.combo import ComboStore
from finalproject.store.combo_item import ComboItemStore
from finalproject.store.product import ProductStore
from finalproject.store.product_discount import ProductDiscountStore
from finalproject.store.receipt_discount import ReceiptDiscountStore
from finalproject.store.store import RecordNotFound
from tests.service.service_utils import generate_id


class CampaignService:
    def __init__(
        self,
        product_store: ProductStore,
        buy_n_get_n_store: BuyNGetNStore,
        combo_store: ComboStore,
        combo_item_store: ComboItemStore,
        product_discount_store: ProductDiscountStore,
        receipt_discount_store: ReceiptDiscountStore,
    ):
        self.product_store = product_store
        self.buy_n_get_n_store = buy_n_get_n_store
        self.combo_store = combo_store
        self.combo_item_store = combo_item_store
        self.product_discount_store = product_discount_store
        self.receipt_discount_store = receipt_discount_store

    def add_combo(self, combo: Combo) -> Combo:
        for combo_item in combo.items:
            self._validate_product(combo_item.product_id)

        combo.id = generate_id()
        self.combo_store.add(combo.to_record())
        for combo_item in combo.items:
            combo_item.id = generate_id()
            self.combo_item_store.add(combo_item.to_record(combo.id))

        return combo

    def get_combo(self, combo_id: str) -> Combo:
        try:
            combo_record = self.combo_store.get_by_id(combo_id)
            combo_item_records = self.combo_item_store.filter_by_field(
                "combo_id", combo_id
            )
            combo_items = [ComboItem.from_record(item) for item in combo_item_records]
            combo = Combo.from_record(combo_record, combo_items)
            return combo
        except RecordNotFound:
            raise ComboNotFound(combo_id)

    def get_all_combos(self) -> list[Combo]:
        combo_records = self.combo_store.list_all()
        combos = []
        for record in combo_records:
            combo_item_records = self.combo_item_store.filter_by_field(
                "combo_id", record.id
            )
            combo_items = [ComboItem.from_record(item) for item in combo_item_records]
            combo = Combo.from_record(record, combo_items)
            combos.append(combo)
        return combos

    def remove_combo(self, combo_id: str) -> None:
        try:
            self.combo_store.remove(combo_id)
        except RecordNotFound:
            raise ComboNotFound(combo_id)

        combo_item_records = self.combo_item_store.filter_by_field("combo_id", combo_id)
        for record in combo_item_records:
            self.combo_item_store.remove(record.id)

    def add_product_discount(
        self, product_discount: ProductDiscount
    ) -> ProductDiscount:
        self._validate_product(product_discount.product_id)
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

    def add_buy_n_get_n(self, buy_n_get_n: BuyNGetN) -> BuyNGetN:
        self._validate_product(buy_n_get_n.buy_product_id)
        self._validate_product(buy_n_get_n.get_product_id)
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

    def add_receipt_discount(
        self, receipt_discount: ReceiptDiscount
    ) -> ReceiptDiscount:
        receipt_discount.id = generate_id()
        self.receipt_discount_store.add(receipt_discount.to_record())
        return receipt_discount

    def get_receipt_discount(self, receipt_discount_id: str) -> ReceiptDiscount:
        try:
            receipt_discount_record = self.receipt_discount_store.get_by_id(
                receipt_discount_id
            )
            receipt_discount = ReceiptDiscount.from_record(receipt_discount_record)
            return receipt_discount
        except RecordNotFound:
            raise ReceiptDiscountNotFound(receipt_discount_id)

    def get_all_receipt_discounts(self) -> list[ReceiptDiscount]:
        receipt_discount_records = self.receipt_discount_store.list_all()
        receipt_discounts = [
            ReceiptDiscount.from_record(record) for record in receipt_discount_records
        ]
        return receipt_discounts

    def remove_receipt_discount(self, receipt_discount_id: str) -> None:
        try:
            self.receipt_discount_store.remove(receipt_discount_id)
        except RecordNotFound:
            raise ReceiptDiscountNotFound(receipt_discount_id)

    def _validate_product(self, product_id: str) -> None:
        try:
            self.product_store.get_by_id(product_id)
        except RecordNotFound:
            raise ProductNotFound(product_id)
