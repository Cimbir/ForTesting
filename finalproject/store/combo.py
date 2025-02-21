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
class ComboItem:
    product_id: str
    quantity: int


@dataclass(frozen=True)
class ComboRecord(Record):
    id: str
    name: str
    discount: float
    combo_list: list[ComboItem]


class ComboStore(BasicStore[ComboRecord], RemovableStore, Protocol):
    """
    Add methods unique to ComboStore here
    """

    pass


class ComboSQLiteStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS combos (
                id TEXT PRIMARY KEY,
                name TEXT,
                discount REAL
            );
            """
        )
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS combo_items (
                combo_id TEXT,
                product_id TEXT,
                quantity INTEGER,
                PRIMARY KEY (combo_id, product_id),
                FOREIGN KEY (combo_id) REFERENCES combos(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            );
            """
        )
        self._conn.commit()

    def add(self, record: ComboRecord) -> ComboRecord:
        try:
            self._conn.execute(
                """
                    INSERT INTO combos(id, name, discount)
                    VALUES (?, ?, ?);
                """,
                (
                    record.id,
                    record.name,
                    record.discount,
                ),
            )
        except sqlite3.IntegrityError:
            raise RecordAlreadyExists()

        for combo_item in record.combo_list:
            self._conn.execute(
                """
                    INSERT INTO combo_items(combo_id, product_id, quantity)
                    VALUES (?, ?, ?);
                """,
                (record.id, combo_item.product_id, combo_item.quantity),
            )

        self._conn.commit()
        return record

    def get_by_id(self, unique_id: str) -> ComboRecord:
        record = self._conn.execute(
            """
                SELECT id, name, discount FROM combos WHERE id = ?;
            """,
            (unique_id,),
        ).fetchone()

        if record is None:
            raise RecordNotFound()

        combo_items = self._conn.execute(
            """
                SELECT product_id, quantity FROM combo_items WHERE combo_id = ?;
            """,
            (unique_id,),
        ).fetchall()

        combo_list = [
            ComboItem(product_id=record[0], quantity=record[1])
            for record in combo_items
        ]

        return ComboRecord(
            id=record[0], name=record[1], discount=record[2], combo_list=combo_list
        )

    def list_all(self) -> list[ComboRecord]:
        records = self._conn.execute(
            """
                SELECT id, name, discount FROM combos;
            """
        ).fetchall()

        result = []
        for record in records:
            combo_items = self._conn.execute(
                """
                    SELECT product_id, quantity FROM combo_items WHERE combo_id = ?;
                """,
                (record[0],),
            ).fetchall()

            combo_list = [
                ComboItem(product_id=record[0], quantity=record[1])
                for record in combo_items
            ]
            combo_record = ComboRecord(
                id=record[0], name=record[1], discount=record[2], combo_list=combo_list
            )
            result.append(combo_record)

        return result

    def remove(self, unique_id: str) -> None:
        cursor = self._conn.execute(
            """
                DELETE FROM combos WHERE id = ?;
            """,
            (unique_id,),
        )

        if cursor.rowcount == 0:
            raise RecordNotFound()

        self._conn.execute(
            """
                DELETE FROM combo_items WHERE combo_id = ?;
            """,
            (unique_id,),
        )
        self._conn.commit()
