from dataclasses import dataclass

from finalproject.models.campaigns import ReceiptDiscount
from finalproject.service.exceptions import ReceiptDiscountNotFound
from finalproject.service.store_utils import generate_id
from finalproject.store.receipt_discount import ReceiptDiscountStore
from finalproject.store.store import RecordNotFound


@dataclass
class ReceiptDiscountService:
    receipt_discount_store: ReceiptDiscountStore

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
