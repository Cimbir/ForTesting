import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.sqlstore import SQLUpdatableStore
from finalproject.store.store import (
    BasicStore,
    Record,
    RecordAlreadyExists,
    RecordNotFound,
    UpdatableStore,
)


@dataclass(frozen=True)
class ShiftRecord(Record):
    id: str
    status: str
    start_time: str
    end_time: str


class ShiftStore(BasicStore[ShiftRecord], UpdatableStore[ShiftRecord], Protocol):
    pass


class ShiftSQLiteStore(SQLUpdatableStore[ShiftRecord]):
    def __init__(self, connection: sqlite3.Connection) -> None:
        super().__init__(connection, "shift")

    def _create_table(self) -> None:
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS shift (
                id TEXT PRIMARY KEY,
                status TEXT,
                start_time TEXT,
                end_time TEXT
            );
            """
        )
        self._conn.commit()

    def _columns(self) -> list[str]:
        return ["id", "status", "start_time", "end_time"]

    def _record_to_row(self, record: ShiftRecord) -> tuple:
        return (record.id, record.status, record.start_time, record.end_time)

    def _row_to_record(self, row: tuple) -> ShiftRecord:
        return ShiftRecord(*row)

