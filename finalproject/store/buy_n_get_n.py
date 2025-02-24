import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.sqlstore import SQLRemovableStore
from finalproject.store.store import (
    BasicStore,
    Record,
    RemovableStore,
)


@dataclass(frozen=True)
class BuyNGetNRecord(Record):
    id: str
    buy_product_id: str
    buy_product_n: int
    get_product_id: str
    get_product_n: int


class BuyNGetNStore(BasicStore[BuyNGetNRecord], RemovableStore, Protocol):
    def get_by_product_id(self, product_id: str) -> list[BuyNGetNRecord]:
        pass


class BuyNGetNSQLiteStore(SQLRemovableStore[BuyNGetNRecord]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, "buy_n_get_n")

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS buy_n_get_n (
                id TEXT PRIMARY KEY,
                buy_product_id TEXT,
                buy_product_n INTEGER,
                get_product_id TEXT,
                get_product_n INTEGER
            );
            """
        )
        self._conn.commit()

    def _record_to_row(self, record: BuyNGetNRecord) -> tuple[str, str, int, str, int]:
        return (
            record.id,
            record.buy_product_id,
            record.buy_product_n,
            record.get_product_id,
            record.get_product_n,
        )

    def _row_to_record(self, row: tuple[str, str, int, str, int]) -> BuyNGetNRecord:
        return BuyNGetNRecord(*row)

    def get_by_product_id(self, product_id: str) -> list[BuyNGetNRecord]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT * FROM buy_n_get_n
            WHERE buy_product_id = ?;
            """,
            (product_id,),
        )

        return [self._row_to_record(row) for row in cursor.fetchall()]
