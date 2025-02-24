import pytest
from finalproject.service.receipt_close.default_receipt_close import DefaultReceiptClose


@pytest.fixture
def def_rec_close() -> DefaultReceiptClose:
    return DefaultReceiptClose()