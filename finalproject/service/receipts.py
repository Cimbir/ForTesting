from finalproject.models.models import Receipt, ReceiptItem
from finalproject.service.exceptions import (
    ProductNotFound,
    ReceiptAlreadyExists,
    ReceiptItemNotFound,
    ReceiptNotFound,
    ShiftNotFound,
)
from finalproject.store.product import ProductStore
from finalproject.store.receipt import ReceiptStore
from finalproject.store.receipt_item import ReceiptItemStore
from finalproject.store.shift import ShiftStore
from finalproject.store.store import RecordAlreadyExists, RecordNotFound
from tests.service.service_utils import generate_id


class ReceiptService:
    def __init__(
        self,
        receipt_store: ReceiptStore,
        receipt_item_store: ReceiptItemStore,
        shift_store: ShiftStore,
        product_store: ProductStore,
    ):
        self.receipt_store = receipt_store
        self.receipt_item_store = receipt_item_store
        self.shift_store = shift_store
        self.product_store = product_store

    def add_receipt(self, receipt: Receipt) -> Receipt:
        self._validate_shift(receipt.shift_id)
        self._add_receipt_to_store(receipt)
        self._add_items_to_receipt(receipt)
        return receipt

    def get_receipt(self, receipt_id: str) -> Receipt:
        try:
            receipt_record = self.receipt_store.get_by_id(receipt_id)
            receipt_item_records = self.receipt_item_store.get_by_receipt_id(receipt_id)
            receipt_items = [
                ReceiptItem.from_record(item) for item in receipt_item_records
            ]
            receipt = Receipt.from_record(receipt_record, receipt_items)
            return receipt
        except RecordNotFound:
            raise ReceiptNotFound(receipt_id)

    def get_all_receipts(self) -> list[Receipt]:
        receipt_records = self.receipt_store.list_all()
        receipts = []
        for record in receipt_records:
            receipt_item_records = self.receipt_item_store.get_by_receipt_id(record.id)
            receipt_items = [
                ReceiptItem.from_record(item) for item in receipt_item_records
            ]
            receipt = Receipt.from_record(record, receipt_items)
            receipts.append(receipt)
        return receipts

    def get_receipts_by_shift_id(self, shift_id: str) -> list[Receipt]:
        self._validate_shift(shift_id)
        receipt_records = self.receipt_store.get_by_shift_id(shift_id)
        receipts = []
        for record in receipt_records:
            receipt_item_records = self.receipt_item_store.get_by_receipt_id(record.id)
            receipt_items = [
                ReceiptItem.from_record(item) for item in receipt_item_records
            ]
            receipt = Receipt.from_record(record, receipt_items)
            receipts.append(receipt)
        return receipts

    def close_receipt(self, receipt_id: str, paid: float) -> Receipt:
        try:
            self.receipt_store.close_receipt_by_id(receipt_id, paid)
            return self.get_receipt(receipt_id)
        except RecordNotFound:
            raise ReceiptNotFound(receipt_id)

    def add_item_to_receipt(self, receipt_id: str, item: ReceiptItem) -> Receipt:
        self._validate_product(item.product_id)
        try:
            self.receipt_store.get_by_id(receipt_id)
            self.receipt_item_store.add(item.to_record(receipt_id))
            return self.get_receipt(receipt_id)
        except RecordNotFound:
            raise ReceiptNotFound(receipt_id)

    def update_item_in_receipt(self, receipt_id: str, item: ReceiptItem) -> Receipt:
        self._validate_product(item.product_id)
        try:
            self.receipt_store.get_by_id(receipt_id)
            self.receipt_item_store.update(item.to_record(receipt_id))
            return self.get_receipt(receipt_id)
        except RecordNotFound:
            raise ReceiptNotFound(receipt_id)

    def remove_item_from_receipt(self, receipt_id: str, item_id: str) -> None:
        try:
            self.receipt_store.get_by_id(receipt_id)
        except RecordNotFound:
            raise ReceiptNotFound(receipt_id)

        try:
            self.receipt_item_store.remove(item_id)
        except RecordNotFound:
            raise ReceiptItemNotFound(item_id)

        return None

    def _validate_shift(self, shift_id: str) -> None:
        try:
            self.shift_store.get_by_id(shift_id)
        except RecordNotFound:
            raise ShiftNotFound(shift_id)

    def _add_receipt_to_store(self, receipt: Receipt) -> None:
        try:
            receipt.id = generate_id()
            self.receipt_store.add(receipt.to_record())
        except RecordAlreadyExists:
            raise ReceiptAlreadyExists(receipt.id)

    def _add_items_to_receipt(self, receipt: Receipt) -> None:
        for item in receipt.items:
            item.id = generate_id()
            self._validate_product(item.product_id)
            self.receipt_item_store.add(item.to_record(receipt.id))

    def _validate_product(self, product_id: str) -> None:
        try:
            self.product_store.get_by_id(product_id)
        except RecordNotFound:
            raise ProductNotFound(product_id)
