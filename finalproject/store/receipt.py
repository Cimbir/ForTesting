import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.store import BasicStore, Record, RecordNotFound


@dataclass(frozen=True)
class ItemRecord(Record):
    id: str
    product_id: str
    quantity: int
    price: float


@dataclass(frozen=True)
class ReceiptRecord(Record):
    id: str
    open: bool
    items: list[ItemRecord]


class ReceiptStore(BasicStore[ReceiptRecord], Protocol):
    def close_receipt_by_id(self, unique_id: str) -> None:
        pass

    def add_item_to_receipt(self, receipt_id: str, item: ItemRecord) -> ItemRecord:
        pass

    def update_item_in_receipt(self, receipt_id: str, item: ItemRecord) -> ItemRecord:
        pass

    def remove_item_from_receipt(self, item_id: str) -> None:
        pass


class ReceiptSQLiteStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS receipts (
                id TEXT PRIMARY KEY,
                open BOOLEAN
            );
            """
        )
        self._conn.commit()

        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id TEXT PRIMARY KEY,
                receipt_id TEXT,
                product_id TEXT,
                quantity INTEGER,
                price REAL
            );
            """
        )
        self._conn.commit()

    def add(self, record: ReceiptRecord) -> ReceiptRecord:
        self._conn.execute(
            """
                INSERT INTO receipts(id, open)
                VALUES (?, ?);
            """,
            (
                record.id,
                record.open,
            ),
        )

        for item in record.items:
            self._conn.execute(
                """
                    INSERT INTO items(id, receipt_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?, ?);
                """,
                (
                    item.id,
                    record.id,
                    item.product_id,
                    item.quantity,
                    item.price,
                ),
            )

        self._conn.commit()

        return record

    def get_by_id(self, unique_id: str) -> ReceiptRecord:
        cursor = self._conn.execute(
            """
            SELECT id, open
            FROM receipts
            WHERE id = ?;
            """,
            (unique_id,),
        )

        receipt = cursor.fetchone()
        if receipt is None:
            raise RecordNotFound()

        cursor = self._conn.execute(
            """
            SELECT id, product_id, quantity, price
            FROM items
            WHERE receipt_id = ?;
            """,
            (unique_id,),
        )

        items = []
        for item in cursor.fetchall():
            items.append(ItemRecord(*item))

        return ReceiptRecord(receipt[0], receipt[1], items)

    def list_all(self) -> list[ReceiptRecord]:
        cursor = self._conn.execute(
            """
            SELECT id, open
            FROM receipts;
            """
        )

        receipts = []
        for receipt in cursor.fetchall():
            cursor = self._conn.execute(
                """
                SELECT id, product_id, quantity, price
                FROM items
                WHERE receipt_id = ?;
                """,
                (receipt[0],),
            )

            items = []
            for item in cursor.fetchall():
                items.append(ItemRecord(*item))

            receipts.append(ReceiptRecord(receipt[0], receipt[1], items))

        return receipts

    def close_receipt_by_id(self, unique_id: str) -> None:
        if (
            self._conn.execute(
                """
            UPDATE receipts
            SET open = 0
            WHERE id = ?;
            """,
                (unique_id,),
            ).rowcount
            == 0
        ):
            raise RecordNotFound()

        self._conn.commit()

    def add_item_to_receipt(self, receipt_id: str, item: ItemRecord) -> ItemRecord:
        if (
            self._conn.execute(
                """
            SELECT id
            FROM receipts
            WHERE id = ?;
            """,
                (receipt_id,),
            ).fetchone()
            is None
        ):
            raise RecordNotFound()

        self._conn.execute(
            """
            INSERT INTO items(id, receipt_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                item.id,
                receipt_id,
                item.product_id,
                item.quantity,
                item.price,
            ),
        )
        self._conn.commit()

        return item

    def update_item_in_receipt(self, receipt_id: str, item: ItemRecord) -> ItemRecord:
        if (
            self._conn.execute(
                """
            UPDATE items
            SET quantity = ?, price = ?
            WHERE product_id = ? AND receipt_id = ?;
            """,
                (
                    item.quantity,
                    item.price,
                    item.product_id,
                    receipt_id,
                ),
            ).rowcount
            == 0
        ):
            raise RecordNotFound()

        self._conn.commit()

        return item

    def remove_item_from_receipt(self, item_id: str) -> None:
        if (
            self._conn.execute(
                """
            DELETE FROM items
            WHERE id = ?;
            """,
                (item_id,),
            ).rowcount
            == 0
        ):
            raise RecordNotFound()

        self._conn.commit()

        return None
