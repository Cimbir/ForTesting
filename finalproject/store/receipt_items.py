import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.sqlstore import SQLBasicStore, SQLUpdatableStore, SQLRemovableStore
from finalproject.store.store import BasicStore, Record, RecordNotFound, UpdatableStore, RemovableStore


@dataclass(frozen=True)
class ReceiptItemRecord(Record):
    id: str
    receipt_id: str
    product_id: str
    quantity: int
    price: float



class ReceiptItemStore(BasicStore[ReceiptItemRecord], UpdatableStore, RemovableStore, Protocol):
    def get_by_receipt_id(self, receipt_id: str) -> list[ReceiptItemRecord]:
        pass

class ReceiptItemSQLiteStore(SQLUpdatableStore[ReceiptItemRecord], SQLRemovableStore[ReceiptItemRecord]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, "receipt_item")

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS receipt_items (
                id TEXT PRIMARY KEY,
                receipt_id TEXT,
                product_id TEXT,
                quantity INTEGER,
                price REAL
            );
            """
        )
        self._conn.commit()

    def _columns(self) -> list[str]:
        return ["id", "receipt_id", "product_id", "quantity", "price"]

    def _record_to_row(self, record: ReceiptItemRecord) -> tuple:
        return record.id, record.receipt_id, record.product_id, record.quantity, record.price

    def _row_to_record(self, row: tuple) -> ReceiptItemRecord:
        return ReceiptItemRecord(*row)

    def get_by_receipt_id(self, receipt_id: str) -> list[ReceiptItemRecord]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT * FROM receipt_items
            WHERE receipt_id = ?;
            """,
            (receipt_id,),
        )

        return [self._row_to_record(row) for row in cursor.fetchall()]