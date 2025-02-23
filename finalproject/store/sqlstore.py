import sqlite3
from typing import Any

from finalproject.store.store import (
    BasicStore,
    RecordAlreadyExists,
    RecordNotFound,
    RecordT,
)


class SQLBasicStore(BasicStore[RecordT]):
    def __init__(self, conn: sqlite3.Connection, table_name: str):
        self._conn = conn
        self.table_name = table_name
        self._create_table()

    def _create_table(self) -> None:
        raise NotImplementedError

    def _row_to_record(self, row: tuple[Any, ...]) -> RecordT:
        raise NotImplementedError

    def _record_to_row(self, record: RecordT) -> tuple[Any, ...]:
        raise NotImplementedError

    def add(self, record: RecordT) -> RecordT:
        self._create_table()
        try:
            self.get_by_id(record.id)
            raise RecordAlreadyExists()
        except RecordNotFound:
            record_row = self._record_to_row(record)
            self._conn.execute(
                f"INSERT INTO {self.table_name} VALUES "
                f"({', '.join(['?'] * len(record_row))})",
                record_row,
            )
            self._conn.commit()
            return record

    def list_all(self) -> list[RecordT]:
        self._create_table()
        cursor = self._conn.execute(f"SELECT * FROM {self.table_name}")
        return [self._row_to_record(row) for row in cursor.fetchall()]

    def get_by_id(self, record_id: str) -> RecordT:
        self._create_table()
        cursor = self._conn.execute(
            f"SELECT * FROM {self.table_name} WHERE id = ?", (record_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise RecordNotFound()
        return self._row_to_record(row)

    def filter_by_field(self, field: str, value: str) -> list[RecordT]:
        self._create_table()
        cursor = self._conn.execute(
            f"SELECT * FROM {self.table_name} WHERE {field} = ?", (value,)
        )
        return [self._row_to_record(row) for row in cursor.fetchall()]


class SQLUpdatableStore(SQLBasicStore[RecordT]):
    def _columns(self) -> list[str]:
        raise NotImplementedError()

    def _update_record(self, record: RecordT) -> None:
        record_row = self._record_to_row(record)
        record_id = record_row[0]
        record_data = record_row[1:]
        columns = self._columns()
        set_part = ", ".join([f"{col} = ?" for col in columns[1:]])
        self._conn.execute(
            f"UPDATE {self.table_name} SET {set_part} WHERE id = ?",
            (*record_data, record_id),
        )

    def update(self, record: RecordT) -> RecordT:
        self._create_table()
        if self.get_by_id(record.id) is None:
            raise RecordNotFound()
        self._update_record(record)
        self._conn.commit()
        return record


class SQLRemovableStore(SQLBasicStore[RecordT]):
    def remove(self, record_id: str) -> None:
        if (
            self._conn.execute(
                f"DELETE FROM {self.table_name} WHERE id = ?", (record_id,)
            ).rowcount
            == 0
        ):
            raise RecordNotFound()
        self._conn.commit()
