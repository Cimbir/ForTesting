import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.sqlstore import SQLUpdatableStore
from finalproject.store.store import (
    BasicStore,
    Record,
    UpdatableStore,
)


@dataclass(frozen=True)
class ProductRecord(Record):
    id: str
    name: str
    price: float


# ProductStore interface IMPORTANT! Put Protocol in the end
class ProductStore(BasicStore[ProductRecord], UpdatableStore[ProductRecord], Protocol):
    """
    Add methods unique to ProductStore here
    """

    pass


class ProductSQLiteStore(SQLUpdatableStore[ProductRecord]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, "product")

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS product (
                id TEXT PRIMARY KEY,
                name TEXT,
                price REAL
            );
            """
        )
        self._conn.commit()

    def _columns(self) -> list[str]:
        return ["id", "name", "price"]

    def _record_to_row(self, record: ProductRecord) -> tuple[str, str, float]:
        return record.id, record.name, record.price

    def _row_to_record(self, row: tuple[str, str, float]) -> ProductRecord:
        return ProductRecord(*row)
