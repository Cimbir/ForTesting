import sqlite3
from typing import Protocol

from finalproject.store.product import ProductSQLiteStore, ProductStore


class StoreDistributor(Protocol):
    def products(self) -> ProductStore:
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
        # Add new stores here

        self._connection = connection

    def products(self) -> ProductStore:
        return self._products

    def destruct(self) -> None:
        self._connection.close()
