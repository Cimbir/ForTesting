import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.sqlstore import SQLBasicStore
from finalproject.store.store import BasicStore, Record, RecordNotFound


@dataclass(frozen=True)
class ReceiptRecord(Record):
    id: str
    open: bool
    paid: float
    shift_id: str



class ReceiptStore(BasicStore[ReceiptRecord], Protocol):
    def get_by_shift_id(self, shift_id: str) -> list[ReceiptRecord]:
        pass

    def close_receipt_by_id(self, unique_id: str, paid: float) -> None:
        pass



class ReceiptSQLiteStore(SQLBasicStore[ReceiptRecord]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, "receipt")

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS receipt (
                id TEXT PRIMARY KEY,
                open BOOLEAN,
                paid REAL,
                shift_id TEXT
            );
            """
        )
        self._conn.commit()

    def _record_to_row(self, record: ReceiptRecord) -> tuple:
        return record.id, record.open, record.paid, record.shift_id

    def _row_to_record(self, row: tuple) -> ReceiptRecord:
        return ReceiptRecord(*row)

    def get_by_shift_id(self, shift_id: str) -> list[ReceiptRecord]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT * FROM receipt
            WHERE shift_id = ?;
            """,
            (shift_id,),
        )

        return [self._row_to_record(row) for row in cursor.fetchall()]

    def close_receipt_by_id(self, unique_id: str, paid: float) -> None:
        if (
            self._conn.execute(
                """
            UPDATE receipts
            SET open = 0, paid = ?
            WHERE id = ?;
            """,
                (paid, unique_id),
            ).rowcount
            == 0
        ):
            raise RecordNotFound()

        self._conn.commit()