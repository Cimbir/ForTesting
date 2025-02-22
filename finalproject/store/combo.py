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
class ComboRecord(Record):
    id: str
    name: str
    discount: float


class ComboStore(BasicStore[ComboRecord], RemovableStore, Protocol):
    """
    Add methods unique to ComboStore here
    """

    pass


class ComboSQLiteStore(SQLRemovableStore[ComboRecord]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, "combo")

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS combo (
                id TEXT PRIMARY KEY,
                name TEXT,
                discount REAL
            );
            """
        )
        self._conn.commit()

    def _record_to_row(self, record: ComboRecord) -> tuple:
        return record.id, record.name, record.discount

    def _row_to_record(self, row: tuple) -> ComboRecord:
        return ComboRecord(*row)