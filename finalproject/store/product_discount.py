import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.store import Record, BasicStore, RemovableStore, RecordAlreadyExists, RecordNotFound


@dataclass(frozen=True)
class ProductDiscountRecord(Record):
    id: str
    product_id: str
    discount: float

class ProductDiscountStore(BasicStore[ProductDiscountRecord], RemovableStore, Protocol):
    def get_by_product_id(self, product_id: str) -> list[ProductDiscountRecord]:
        pass

class ProductDiscountSQLiteStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS discounts (
                id TEXT PRIMARY KEY,
                product_id TEXT,
                discount REAL
            );
            """
        )
        self._conn.commit()

    def add(self, record: ProductDiscountRecord) -> ProductDiscountRecord:
        try:
            self._conn.execute(
                """
                INSERT INTO discounts(
                id,
                product_id,
                discount)
                VALUES (?, ?, ?);
                """,
                (
                    record.id,
                    record.product_id,
                    record.discount,
                ),
            )
        except sqlite3.IntegrityError:
            raise RecordAlreadyExists()

        self._conn.commit()
        return record

    def get_by_id(self, unique_id: str) -> ProductDiscountRecord:
        cursor = self._conn.execute(
            """
            SELECT id, product_id, discount
            FROM discounts
            WHERE id = ?;
            """,
            (unique_id,),
        )
        row = cursor.fetchone()
        if row is None:
            raise RecordNotFound()
        return ProductDiscountRecord(*row)

    def list_all(self) -> list[ProductDiscountRecord]:
        cursor = self._conn.execute(
            """
            SELECT id, product_id, discount
            FROM discounts;
            """
        )
        return [ProductDiscountRecord(*row) for row in cursor.fetchall()]

    def remove(self, unique_id: str) -> None:
        if (
            self._conn.execute(
                """
                DELETE FROM discounts
                WHERE id = ?;
                """,
                (unique_id,),
            ).rowcount == 0
        ):
            raise RecordNotFound()
        self._conn.commit()

    def get_by_product_id(self, product_id: str) -> list[ProductDiscountRecord]:
        cursor = self._conn.execute(
            """
            SELECT id, product_id, discount
            FROM discounts
            WHERE product_id = ?;
            """,
            (product_id,),
        )
        return [ProductDiscountRecord(*row) for row in cursor.fetchall()]

