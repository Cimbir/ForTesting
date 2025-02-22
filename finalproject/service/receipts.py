from finalproject.models.models import Receipt, ReceiptItem
from finalproject.store.receipt import ReceiptStore, ReceiptRecord
from finalproject.store.receipt_items import ReceiptItemStore, ReceiptItemRecord
from finalproject.store.store import RecordAlreadyExists, RecordNotFound

class ReceiptService:
    def __init__(
        self,
        receipt_store: ReceiptStore,
        receipt_item_store: ReceiptItemStore,
    ):
        self.receipt_store = receipt_store
        self.receipt_item_store = receipt_item_store

    def add_receipt(self, receipt: Receipt) -> bool:
        try:
            self.receipt_store.add(receipt.to_record())
            for item in receipt.items:
                self.receipt_item_store.add(item.to_record())
            return True
        except RecordAlreadyExists:
            return False

    def get_receipt(self, receipt_id: str) -> Receipt | None:
        try:
            receipt_record = self.receipt_store.get_by_id(receipt_id)
            receipt_item_records = self.receipt_item_store.get_by_receipt_id(receipt_id)
            receipt_items = [ReceiptItem.from_record(item) for item in receipt_item_records]
            receipt = Receipt.from_record(receipt_record, receipt_items)
            return receipt
        except RecordNotFound:
            raise None

    def get_receipts_by_shift_id(self, shift_id: str) -> list[Receipt]:
        receipt_records = self.receipt_store.get_by_shift_id(shift_id)
        receipts = []
        for record in receipt_records:
            receipt_item_records = self.receipt_item_store.get_by_receipt_id(record.id)
            receipt_items = [ReceiptItem.from_record(item) for item in receipt_item_records]
            receipt = Receipt.from_record(record, receipt_items)
            receipts.append(receipt)
        return receipts

    def close_receipt(self, receipt_id: str, paid: float) -> bool:
        try:
            self.receipt_store.close_receipt_by_id(receipt_id, paid)
            return True
        except RecordNotFound:
            return False

    def add_item_to_receipt(self, receipt_id: str, item: ReceiptItem) -> bool:
        try:
            self.receipt_store.get_by_id(receipt_id)
            self.receipt_item_store.add(item.to_record())
            return True
        except RecordNotFound:
            return False

    def update_item_in_receipt(self, receipt_id: str, item: ReceiptItem) -> bool:
        try:
            self.receipt_store.get_by_id(receipt_id)
            self.receipt_item_store.update(item.to_record())
            return True
        except RecordNotFound:
            return False

    def remove_item_from_receipt(self, receipt_id:str, item_id: str) -> bool:
        try:
            self.receipt_store.get_by_id(receipt_id)
            self.receipt_item_store.remove(item_id)
            return True
        except RecordNotFound:
            return False
