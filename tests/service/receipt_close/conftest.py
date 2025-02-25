import pytest

from finalproject.service.receipt_close.default_receipt_close import DefaultReceiptClose
from finalproject.service.receipt_close.receipt_close import ReceiptClose


@pytest.fixture
def def_rec_close() -> ReceiptClose:
    return DefaultReceiptClose()
