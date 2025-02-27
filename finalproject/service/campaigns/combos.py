from dataclasses import dataclass

from finalproject.models.campaigns import Combo, ComboItem
from finalproject.service.exceptions import ComboNotFound
from finalproject.service.store_utils import _validate_product, generate_id
from finalproject.store.combo import ComboStore
from finalproject.store.combo_item import ComboItemStore
from finalproject.store.product import ProductStore
from finalproject.store.store import RecordNotFound


@dataclass
class ComboService:
    product_store: ProductStore
    combo_store: ComboStore
    combo_item_store: ComboItemStore

    def add_combo(self, combo: Combo) -> Combo:
        for combo_item in combo.items:
            _validate_product(self.product_store, combo_item.product_id)

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
