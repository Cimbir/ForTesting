import sqlite3
from dataclasses import dataclass

from finalproject.store.store import BasicStore, Record, UpdatableStore


@dataclass(frozen=True)
class ProductRecord(Record):
    id: str
    name: str
    price: float
    is_removed: bool


# ProductStore interface
class ProductStore(BasicStore[ProductRecord], UpdatableStore[ProductRecord]):
    """
    Add methods unique to ProductStore here
    """

    pass


class ProductSQLiteStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        raise NotImplementedError()

    def add(self, record: ProductRecord) -> ProductRecord:
        raise NotImplementedError()

    def get_by_id(self, unique_id: str) -> ProductRecord:
        raise NotImplementedError()

    def list_all(self) -> list[ProductRecord]:
        raise NotImplementedError()

    def update(self, record: ProductRecord) -> ProductRecord:
        raise NotImplementedError()
