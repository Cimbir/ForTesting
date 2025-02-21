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
class BuyNGetNRecord(Record):
    id: str
    buy_product_id: str
    buy_product_n: int
    get_product_id: str
    get_product_n: int


class BuyNGetNStore(BasicStore[BuyNGetNRecord], RemovableStore, Protocol):
    def get_by_product_id(self, product_id: str) -> list[BuyNGetNRecord]:
        pass


class BuyNGetNSQLiteStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

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

    def add(self, record: BuyNGetNRecord) -> BuyNGetNRecord:
        try:
            self._conn.execute(
                """
                    INSERT INTO buy_n_get_n(
                    id, 
                    buy_product_id, 
                    buy_product_n, 
                    get_product_id, 
                    get_product_n)
                    VALUES (?, ?, ?, ?, ?);
                """,
                (
                    record.id,
                    record.buy_product_id,
                    record.buy_product_n,
                    record.get_product_id,
                    record.get_product_n,
                ),
            )
        except sqlite3.IntegrityError:
            raise RecordAlreadyExists()

        self._conn.commit()
        return record

    def get_by_id(self, unique_id: str) -> BuyNGetNRecord:
        cursor = self._conn.execute(
            """
                SELECT id, buy_product_id, buy_product_n, get_product_id, get_product_n
                FROM buy_n_get_n
                WHERE id = ?;
            """,
            (unique_id,),
        )

        record = cursor.fetchone()
        if record is None:
            raise RecordNotFound()

        return BuyNGetNRecord(*record)

    def list_all(self) -> list[BuyNGetNRecord]:
        cursor = self._conn.execute(
            """
                SELECT id, buy_product_id, buy_product_n, get_product_id, get_product_n
                FROM buy_n_get_n;
            """
        )

        return [BuyNGetNRecord(*record) for record in cursor.fetchall()]

    def remove(self, unique_id: str) -> None:
        if (
            self._conn.execute(
                """
            DELETE FROM buy_n_get_n WHERE id = ?;
            """,
                (unique_id,),
            ).rowcount
            == 0
        ):
            raise RecordNotFound()

        self._conn.commit()

    def get_by_product_id(self, product_id: str) -> list[BuyNGetNRecord]:
        cursor = self._conn.execute(
            """
                SELECT id, buy_product_id, buy_product_n, get_product_id, get_product_n
                FROM buy_n_get_n
                WHERE buy_product_id = ?;
            """,
            (product_id,),
        )

        return [BuyNGetNRecord(*record) for record in cursor.fetchall()]
