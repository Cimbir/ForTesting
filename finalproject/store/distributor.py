import sqlite3
from typing import Protocol

from finalproject.store.buy_n_get_n import BuyNGetNSQLiteStore, BuyNGetNStore
from finalproject.store.combo import ComboSQLiteStore, ComboStore
from finalproject.store.combo_item import ComboItemSQLiteStore, ComboItemStore
from finalproject.store.paid_receipt import PaidReceiptSQLiteStore, PaidReceiptStore
from finalproject.store.product import ProductSQLiteStore, ProductStore
from finalproject.store.product_discount import (
    ProductDiscountSQLiteStore,
    ProductDiscountStore,
)
from finalproject.store.receipt import ReceiptSQLiteStore, ReceiptStore
from finalproject.store.receipt_discount import (
    ReceiptDiscountSQLiteStore,
    ReceiptDiscountStore,
)
from finalproject.store.receipt_item import ReceiptItemSQLiteStore, ReceiptItemStore
from finalproject.store.shift import ShiftSQLiteStore, ShiftStore


class StoreDistributor(Protocol):
    def products(self) -> ProductStore:
        pass

    def buy_n_get_n(self) -> BuyNGetNStore:
        pass

    def combos(self) -> ComboStore:
        pass

    def combo_items(self) -> ComboItemStore:
        pass

    def receipt(self) -> ReceiptStore:
        pass

    def receipt_items(self) -> ReceiptItemStore:
        pass

    def receipt_discounts(self) -> ReceiptDiscountStore:
        pass

    def product_discount(self) -> ProductDiscountStore:
        pass

    def shifts(self) -> ShiftStore:
        pass

    def paid_receipts(self) -> PaidReceiptStore:
        pass

    def destruct(self) -> None:
        """
        Closes connection to the database
        """
        pass


class SQLiteStoreDistributor:
    def __init__(self, database: str) -> None:
        connection = sqlite3.connect(database=database, check_same_thread=False)

        self._products = ProductSQLiteStore(connection)
        self._combos = ComboSQLiteStore(connection)
        self._combo_items = ComboItemSQLiteStore(connection)
        self._buy_n_get_n = BuyNGetNSQLiteStore(connection)
        self._receipt = ReceiptSQLiteStore(connection)
        self._receipt_items = ReceiptItemSQLiteStore(connection)
        self._receipt_discounts = ReceiptDiscountSQLiteStore(connection)
        self._product_discount = ProductDiscountSQLiteStore(connection)
        self._shifts = ShiftSQLiteStore(connection)
        self._paid_receipts = PaidReceiptSQLiteStore(connection)

        # Add new stores here

        self._connection = connection

    def products(self) -> ProductStore:
        return self._products

    def buy_n_get_n(self) -> BuyNGetNStore:
        return self._buy_n_get_n

    def combos(self) -> ComboStore:
        return self._combos

    def combo_items(self) -> ComboItemStore:
        return self._combo_items

    def receipt(self) -> ReceiptStore:
        return self._receipt

    def receipt_items(self) -> ReceiptItemStore:
        return self._receipt_items

    def receipt_discounts(self) -> ReceiptDiscountStore:
        return self._receipt_discounts

    def product_discount(self) -> ProductDiscountStore:
        return self._product_discount

    def shifts(self) -> ShiftStore:
        return self._shifts

    def paid_receipts(self) -> PaidReceiptStore:
        return self._paid_receipts

    def destruct(self) -> None:
        self._connection.close()
