import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.store import (
    BasicStore,
    Record,
    RecordAlreadyExists,
    RecordNotFound,
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


class ProductSQLiteStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT,
                price REAL
            );
            """
        )
        self._conn.commit()

    def add(self, record: ProductRecord) -> ProductRecord:
        try:
            self._conn.execute(
                """
                    INSERT INTO products(id, name, price)
                    VALUES (?, ?, ?);
                """,
                (
                    record.id,
                    record.name,
                    record.price,
                ),
            )
        except sqlite3.IntegrityError:
            raise RecordAlreadyExists()

        self._conn.commit()
        return record

    def get_by_id(self, unique_id: str) -> ProductRecord:
        record = self._conn.execute(
            """
                SELECT id, name, price FROM products WHERE id = ?;
            """,
            (unique_id,),
        ).fetchone()

        if record is None:
            raise RecordNotFound()

        return ProductRecord(id=record[0], name=record[1], price=record[2])

    def list_all(self) -> list[ProductRecord]:
        records = self._conn.execute(
            """
                SELECT id, name, price FROM products;
            """
        ).fetchall()

        return [
            ProductRecord(id=record[0], name=record[1], price=record[2])
            for record in records
        ]

    def update(self, record: ProductRecord) -> ProductRecord:
        result = self._conn.execute(
            """
            UPDATE products
            SET name = ?, price = ?
            WHERE id = ?;
            """,
            (
                record.name,
                record.price,
                record.id,
            ),
        )

        if result.rowcount == 0:
            raise RecordNotFound()

        return record
