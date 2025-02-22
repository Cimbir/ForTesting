import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.sqlstore import SQLRemovableStore
from finalproject.store.store import (
    BasicStore,
    Record,
    RecordAlreadyExists,
    RecordNotFound,
    RemovableStore,
)


@dataclass(frozen=True)
class ProductDiscountRecord(Record):
    id: str
    product_id: str
    discount: float


class ProductDiscountStore(BasicStore[ProductDiscountRecord], RemovableStore, Protocol):
    def get_by_product_id(self, product_id: str) -> list[ProductDiscountRecord]:
        pass


class ProductDiscountSQLiteStore(SQLRemovableStore[ProductDiscountRecord]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, "product_discount")

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS product_discount (
                id TEXT PRIMARY KEY,
                product_id TEXT,
                discount REAL
            );
            """
        )
        self._conn.commit()

    def _record_to_row(self, record: ProductDiscountRecord) -> tuple:
        return record.id, record.product_id, record.discount

    def _row_to_record(self, row: tuple) -> ProductDiscountRecord:
        return ProductDiscountRecord(*row)

    def get_by_product_id(self, product_id: str) -> list[ProductDiscountRecord]:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            SELECT * FROM product_discount
            WHERE product_id = ?;
            """,
            (product_id,),
        )

        return [self._row_to_record(row) for row in cursor.fetchall()]