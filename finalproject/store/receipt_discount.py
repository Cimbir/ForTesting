import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.sqlstore import (
    SQLRemovableStore,
)
from finalproject.store.store import (
    BasicStore,
    Record,
    RemovableStore,
)


@dataclass(frozen=True)
class ReceiptDiscountRecord(Record):
    id: str
    minimum_total: float
    discount: float


class ReceiptDiscountStore(BasicStore[ReceiptDiscountRecord], RemovableStore, Protocol):
    pass


class ReceiptDiscountSQLiteStore(SQLRemovableStore[ReceiptDiscountRecord]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, "receipt_discount")

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS receipt_discount (
                id TEXT PRIMARY KEY,
                minimum_total REAL,
                discount REAL
            );
            """
        )
        self._conn.commit()

    def _record_to_row(self, record: ReceiptDiscountRecord) -> tuple[str, float, float]:
        return record.id, record.minimum_total, record.discount

    def _row_to_record(self, row: tuple[str, float, float]) -> ReceiptDiscountRecord:
        return ReceiptDiscountRecord(*row)
