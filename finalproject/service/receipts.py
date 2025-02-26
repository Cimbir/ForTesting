from finalproject.models.campaigns import (
    BuyNGetN,
    Combo,
    ComboItem,
    ProductDiscount,
    ReceiptDiscount,
)
from finalproject.models.models import Receipt, ReceiptItem
from finalproject.service.currency_conversion.currency_conversion import (
    CurrencyConversionService,
)
from finalproject.service.exceptions import (
    ProductNotFound,
    ReceiptAlreadyExists,
    ReceiptItemNotFound,
    ReceiptNotFound,
    ShiftNotFound,
)
from finalproject.service.receipt_close.buy_n_get_n_decorator import BuyNGetNDecorator
from finalproject.service.receipt_close.combo_decorator import ComboDecorator
from finalproject.service.receipt_close.default_receipt_close import DefaultReceiptClose
from finalproject.service.receipt_close.product_discount_decorator import (
    ProductDiscountDecorator,
)
from finalproject.service.receipt_close.receipt_close import ReceiptClose
from finalproject.service.receipt_close.receipt_discount_decorator import (
    ReceiptDiscountDecorator,
)
from finalproject.store.buy_n_get_n import BuyNGetNStore
from finalproject.store.combo import ComboStore
from finalproject.store.combo_item import ComboItemStore
from finalproject.store.product import ProductStore
from finalproject.store.product_discount import ProductDiscountStore
from finalproject.store.receipt import ReceiptStore
from finalproject.store.receipt_discount import ReceiptDiscountStore
from finalproject.store.receipt_item import ReceiptItemRecord, ReceiptItemStore
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
        combo_store: ComboStore,
        combo_item_store: ComboItemStore,
        product_discount_store: ProductDiscountStore,
        receipt_discount_store: ReceiptDiscountStore,
        buy_n_get_n_store: BuyNGetNStore,
        currency_conversion_service: CurrencyConversionService,
    ):
        self.receipt_store = receipt_store
        self.receipt_item_store = receipt_item_store
        self.shift_store = shift_store
        self.product_store = product_store

        self.combo_store = combo_store
        self.combo_item_store = combo_item_store
        self.product_discount_store = product_discount_store
        self.receipt_discount_store = receipt_discount_store
        self.buy_n_get_n_store = buy_n_get_n_store

        self.currency_conversion_service = currency_conversion_service

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

    def close_receipt(self, receipt_id: str, currency_name: str) -> Receipt:
        try:
            receipt = self.get_receipt(receipt_id)
            if not receipt.open:
                return receipt

            close_result = self._build_receipt_close().close(receipt)

            for added_product_id in close_result.added_products:
                self.update_product_in_receipt(
                    receipt_id,
                    added_product_id,
                    close_result.added_products[added_product_id],
                )

            self.receipt_store.close_receipt_by_id(receipt_id)
            return self.get_receipt(receipt_id)
        except RecordNotFound:
            raise ReceiptNotFound(receipt_id)

    def update_product_in_receipt(
        self, receipt_id: str, product_id: str, quantity: int
    ) -> Receipt:
        self._validate_product(product_id)
        try:
            receipt = self.get_receipt(receipt_id)

            if not receipt.open:
                return receipt

            receipt_items = [
                ReceiptItem.from_record(record)
                for record in self.receipt_item_store.get_by_receipt_id(receipt_id)
            ]

            for receipt_item in receipt_items:
                if product_id == receipt_item.product_id:
                    new_quantity = max(receipt_item.quantity + quantity, 0)
                    if new_quantity == 0:
                        self.remove_product_from_receipt(receipt_id, product_id)
                        return self.get_receipt(receipt_id)
                    self.receipt_item_store.update(
                        ReceiptItemRecord(
                            id=receipt_item.id,
                            receipt_id=receipt_id,
                            product_id=product_id,
                            quantity=new_quantity,
                            price=receipt_item.price,
                        )
                    )
                    return self.get_receipt(receipt_id)

            if quantity > 0:
                self.receipt_item_store.add(
                    ReceiptItemRecord(
                        id=generate_id(),
                        receipt_id=receipt_id,
                        product_id=product_id,
                        quantity=quantity,
                        price=self.product_store.get_by_id(product_id).price,
                    )
                )

            return self.get_receipt(receipt_id)
        except RecordNotFound:
            raise ReceiptNotFound(receipt_id)

    def remove_product_from_receipt(self, receipt_id: str, product_id: str) -> None:
        receipt: Receipt

        try:
            receipt = self.get_receipt(receipt_id)
            if not receipt.open:
                return None
        except RecordNotFound:
            raise ReceiptNotFound(receipt_id)

        try:
            for item in receipt.items:
                if item.product_id == product_id:
                    self.receipt_item_store.remove(item.id)
                    return None
        except RecordNotFound:
            raise ReceiptItemNotFound(product_id)

        raise ReceiptItemNotFound(product_id)

    def get_receipt_cost(self, receipt_id: str) -> float:
        try:
            receipt = self.get_receipt(receipt_id)
            return self._build_receipt_close().close(receipt).price
        except RecordNotFound:
            raise ReceiptNotFound(receipt_id)

    def get_receipt_discount_amount(self, receipt_id: str) -> float:
        try:
            receipt = self.get_receipt(receipt_id)
            without_discount = 0.0
            for item in receipt.items:
                without_discount += item.price * item.quantity
            with_discount = self._build_receipt_close().close(receipt).price
            return without_discount - with_discount
        except RecordNotFound:
            raise ReceiptNotFound(receipt_id)

    def _build_receipt_close(self) -> ReceiptClose:
        close: ReceiptClose = DefaultReceiptClose()

        for rec_discount in self.receipt_discount_store.list_all():
            close = ReceiptDiscountDecorator(
                close, ReceiptDiscount.from_record(rec_discount)
            )

        for prod_discount in self.product_discount_store.list_all():
            close = ProductDiscountDecorator(
                close, ProductDiscount.from_record(prod_discount)
            )

        for combo in self.combo_store.list_all():
            close = ComboDecorator(
                close,
                Combo.from_record(
                    combo,
                    [
                        ComboItem.from_record(item)
                        for item in self.combo_item_store.filter_by_field(
                            "combo_id", combo.id
                        )
                    ],
                ),
            )

        for bngn in self.buy_n_get_n_store.list_all():
            close = BuyNGetNDecorator(close, BuyNGetN.from_record(bngn))

        return close

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
