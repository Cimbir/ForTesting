import sqlite3
from typing import Protocol


from finalproject.store.buy_n_get_n import BuyNGetNSQLiteStore, BuyNGetNStore
from finalproject.store.combo import ComboSQLiteStore, ComboStore
from finalproject.store.product import ProductSQLiteStore, ProductStore


class StoreDistributor(Protocol):
    def products(self) -> ProductStore:
        pass

    def buy_n_get_n(self) -> BuyNGetNStore:
        pass
    
    def combos(self) -> ComboStore:
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
        # Add new stores here
        self._buy_n_get_n = BuyNGetNSQLiteStore(connection)

        self._connection = connection

    def products(self) -> ProductStore:
        return self._products

    def buy_n_get_n(self) -> BuyNGetNStore:
        return self._buy_n_get_n
    
    def combos(self) -> ComboStore:
        return self._combos

    def destruct(self) -> None:
        self._connection.close()
