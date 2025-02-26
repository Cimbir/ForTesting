from dataclasses import dataclass
from typing import Protocol

from finalproject.store.store import Record, BasicStore


@dataclass(frozen=True)
class PaidReceiptRecord(Record):
    id: str
    receipt_id: str
    currency_name: str
    paid: float

class PaidReceiptStore(BasicStore[PaidReceiptRecord], Protocol):
    pass