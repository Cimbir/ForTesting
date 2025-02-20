from typing import Protocol, TypeVar


class Record(Protocol):
    id: str


RecordT = TypeVar("RecordT", bound=Record)


class BasicStore(Protocol[RecordT]):
    def add(self, record: RecordT) -> RecordT:
        pass

    def get_by_id(self, unique_id: str) -> RecordT:
        pass

    def list_all(self) -> list[RecordT]:
        pass


class UpdatableStore(Protocol[RecordT]):
    def update(self, record: RecordT) -> RecordT:
        pass


class RemovableStore(Protocol):
    def remove(self, unique_id: str) -> None:
        pass
