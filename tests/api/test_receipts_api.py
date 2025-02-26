from unittest.mock import ANY

from starlette.testclient import TestClient

from finalproject.store.distributor import StoreDistributor
from finalproject.store.shift import ShiftRecord


def test_should_receipt_create(http: TestClient, distributor: StoreDistributor) -> None:
    response = http.post("/receipts", json={"shift_id": "1"})

    assert response.status_code == 201
    assert response.json() == {
        "receipt": {
            "id": ANY,
            "open": True,
            "shift_id": "1",
            "items": [],
        }
    }

def test_should_not_create_receipt_on_invalid_shift(http: TestClient) -> None:
    response = http.post("/receipts", json={"shift_id": "invalid"})

