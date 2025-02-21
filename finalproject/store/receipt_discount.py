import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.store import (
    BasicStore,
    Record,
    RecordAlreadyExists,
    RecordNotFound,
    RemovableStore,
)


@dataclass(frozen=True)
class ReceiptDiscountRecord(Record):
    id: str
    minimum_total: float
    discount: float


class ReceiptDiscountStore(BasicStore[ReceiptDiscountRecord], RemovableStore, Protocol):
    pass


class ReceiptDiscountSQLiteStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

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

    def add(self, record: ReceiptDiscountRecord) -> ReceiptDiscountRecord:
        try:
            self._conn.execute(
                """
                    INSERT INTO receipt_discount(
                    id, 
                    minimum_total,
                    discount)
                    VALUES (?, ?, ?);
                """,
                (
                    record.id,
                    record.minimum_total,
                    record.discount,
                ),
            )
        except sqlite3.IntegrityError:
            raise RecordAlreadyExists()

        self._conn.commit()
        return record

    def get_by_id(self, unique_id: str) -> ReceiptDiscountRecord:
        cursor = self._conn.execute(
            """
                SELECT id, minimum_total, discount
                FROM receipt_discount
                WHERE id = ?;
            """,
            (unique_id,),
        )

        record = cursor.fetchone()
        if record is None:
            raise RecordNotFound()

        return ReceiptDiscountRecord(
            id=record[0], minimum_total=record[1], discount=record[2]
        )

    def list_all(self) -> list[ReceiptDiscountRecord]:
        cursor = self._conn.execute(
            """
                SELECT id, minimum_total, discount
                FROM receipt_discount;
            """
        )

        return [
            ReceiptDiscountRecord(
                id=record[0], minimum_total=record[1], discount=record[2]
            )
            for record in cursor.fetchall()
        ]

    def remove(self, unique_id: str) -> None:
        if (
            self._conn.execute(
                """
            DELETE FROM receipt_discount WHERE id = ?;
            """,
                (unique_id,),
            ).rowcount
            == 0
        ):
            raise RecordNotFound()

        self._conn.commit()
