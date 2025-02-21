import sqlite3
from dataclasses import dataclass
from typing import Protocol

from finalproject.store.store import (
    BasicStore,
    Record,
    RecordAlreadyExists,
    RecordNotFound,
    RemovableStore, UpdatableStore,
)


@dataclass(frozen=True)
class ShiftRecord(Record):
    id: str
    status: str
    start_time: str
    end_time: str

class ShiftStore(BasicStore[ShiftRecord], UpdatableStore[ShiftRecord], Protocol):
    pass


class ShiftSQLiteStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS shift (
                id TEXT PRIMARY KEY,
                status TEXT,
                start_time DATETIME,
                end_time DATETIME
            );
            """
        )
        self._conn.commit()

    def add(self, record: ShiftRecord) -> ShiftRecord:
        try:
            self._conn.execute(
                """
                    INSERT INTO shift(
                    id, 
                    status,
                    start_time,
                    end_time)
                    VALUES (?, ?, ?, ?);
                """,
                (
                    record.id,
                    record.status,
                    record.start_time,
                    record.end_time,
                ),
            )
        except sqlite3.IntegrityError:
            raise RecordAlreadyExists()

        self._conn.commit()
        return record

    def get_by_id(self, unique_id: str) -> ShiftRecord:
        cursor = self._conn.execute(
            """
                SELECT id, status, start_time, end_time
                FROM shift
                WHERE id = ?;
            """,
            (unique_id,),
        )

        record = cursor.fetchone()
        if record is None:
            raise RecordNotFound()

        return ShiftRecord(*record)

    def list_all(self) -> list[ShiftRecord]:
        cursor = self._conn.execute(
            """
                SELECT id, status, start_time, end_time
                FROM shift;
            """
        )

        return [ShiftRecord(*record) for record in cursor.fetchall()]

    def update(self, record: ShiftRecord) -> ShiftRecord:
        result = self._conn.execute(
            """
            UPDATE shift
            SET status = ?, start_time = ?, end_time = ?
            WHERE id = ?;
            """,
            (
                record.status,
                record.start_time,
                record.end_time,
                record.id,
            ),
        )

        if result.rowcount == 0:
            raise RecordNotFound()

        self._conn.commit()
        return record