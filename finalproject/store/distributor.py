import sqlite3
from typing import Protocol

from finalproject.store.buy_n_get_n import BuyNGetNSQLiteStore, BuyNGetNStore
from finalproject.store.combo import ComboSQLiteStore, ComboStore
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
from finalproject.store.shift import ShiftSQLiteStore, ShiftStore


class StoreDistributor(Protocol):
    def products(self) -> ProductStore:
        pass

    def buy_n_get_n(self) -> BuyNGetNStore:
        pass

    def combos(self) -> ComboStore:
        pass

    def receipt(self) -> ReceiptStore:
        pass

    def receipt_discounts(self) -> ReceiptDiscountStore:
        pass

    def product_discount(self) -> ProductDiscountStore:
        pass

    def shifts(self) -> ShiftStore:
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
        self._buy_n_get_n = BuyNGetNSQLiteStore(connection)
        self._receipt = ReceiptSQLiteStore(connection)
        self._receipt_discounts = ReceiptDiscountSQLiteStore(connection)
        self._product_discount = ProductDiscountSQLiteStore(connection)
        self._shifts = ShiftSQLiteStore(connection)

        # Add new stores here

        self._connection = connection

    def products(self) -> ProductStore:
        return self._products

    def buy_n_get_n(self) -> BuyNGetNStore:
        return self._buy_n_get_n

    def combos(self) -> ComboStore:
        return self._combos

    def receipt(self) -> ReceiptStore:
        return self._receipt

    def receipt_discounts(self) -> ReceiptDiscountStore:
        return self._receipt_discounts

    def product_discount(self) -> ProductDiscountStore:
        return self._product_discount

    def shifts(self) -> ShiftStore:
        return self._shifts

    def destruct(self) -> None:
        self._connection.close()
