import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.sqlstore import SQLBasicStore
from finalproject.store.store import BasicStore, Record

PAID_RECEIPT_TABLE_NAME = "paid_receipt"


@dataclass(frozen=True)
class PaidReceiptRecord(Record):
    id: str
    receipt_id: str
    currency_name: str
    paid: float


class PaidReceiptStore(BasicStore[PaidReceiptRecord], Protocol):
    pass


class PaidReceiptSQLiteStore(SQLBasicStore[PaidReceiptRecord]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(conn=connection, table_name=PAID_RECEIPT_TABLE_NAME)

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS paid_receipt (
                id TEXT PRIMARY KEY,
                receipt_id TEXT,
                currency_name TEXT,
                paid REAL
            );
            """
        )
        self._conn.commit()

    def _record_to_row(self, record: PaidReceiptRecord) -> tuple[str, str, str, float]:
        return record.id, record.receipt_id, record.currency_name, record.paid

    def _row_to_record(self, row: tuple[str, str, str, float]) -> PaidReceiptRecord:
        return PaidReceiptRecord(*row)
