import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.sqlstore import SQLRemovableStore
from finalproject.store.store import (
    BasicStore,
    Record,
    RemovableStore,
)


@dataclass(frozen=True)
class ComboItemRecord(Record):
    id: str
    product_id: str
    quantity: int


class ComboItemStore(BasicStore[ComboItemRecord], RemovableStore, Protocol):
    """
    Add methods unique to ComboStore here
    """

    pass


class ComboItemSQLiteStore(SQLRemovableStore[ComboItemRecord]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, "combo_item")

    def _create_table(self) -> None:
        self._conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id TEXT PRIMARY KEY,
                product_id TEXT,
                quantity INTEGER
            );
            """
        )
        self._conn.commit()

    def _record_to_row(self, record: ComboItemRecord) -> tuple[str, str, int]:
        return record.id, record.product_id, record.quantity

    def _row_to_record(self, row: tuple[str, str, int]) -> ComboItemRecord:
        return ComboItemRecord(*row)
