from dataclasses import dataclass

from finalproject.models.models import Model


@dataclass
class PaidReceipt(Model):
    id: str
    receipt_id: str
    currency_name: str
    paid: float