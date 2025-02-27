from unittest.mock import ANY

from starlette.testclient import TestClient

from finalproject.store.distributor import StoreDistributor
from finalproject.store.product_discount import ProductDiscountRecord


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


def test_should_error_on_create_receipt_on_invalid_shift(http: TestClient) -> None:
    response = http.post("/receipts", json={"shift_id": "invalid"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Shift not found"}


def test_should_add_product_to_receipt(
    http: TestClient, distributor: StoreDistributor
) -> None:
    response = http.post("/receipts", json={"shift_id": "1"})
    receipt_id = response.json()["receipt"]["id"]

    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "1", "quantity": 1}
    )

    assert response.status_code == 201
    assert response.json() == {
        "receipt": {
            "id": receipt_id,
            "open": True,
            "shift_id": "1",
            "items": [
                {
                    "id": ANY,
                    "product_id": "1",
                    "quantity": 1,
                    "price": 1.0,
                    "total": 1.0,
                }
            ],
        }
    }

    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "2", "quantity": 2}
    )

    assert response.status_code == 201
    assert response.json() == {
        "receipt": {
            "id": receipt_id,
            "open": True,
            "shift_id": "1",
            "items": [
                {
                    "id": ANY,
                    "product_id": "1",
                    "quantity": 1,
                    "price": 1.0,
                    "total": 1.0,
                },
                {
                    "id": ANY,
                    "product_id": "2",
                    "quantity": 2,
                    "price": 2.0,
                    "total": 4.0,
                },
            ],
        }
    }


def test_should_error_on_add_non_existent_product(http: TestClient) -> None:
    response = http.post("/receipts", json={"shift_id": "1"})
    receipt_id = response.json()["receipt"]["id"]

    response = http.post(
        f"/receipts/{receipt_id}/products",
        json={"product_id": "invalid", "quantity": 1},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}


def test_should_error_on_add_product_to_non_existent_receipt(http: TestClient) -> None:
    response = http.post(
        "/receipts/invalid/products", json={"product_id": "1", "quantity": 1}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}


def test_should_calculate_payment(
    http: TestClient, distributor: StoreDistributor
) -> None:
    response = http.post("/receipts", json={"shift_id": "1"})
    receipt_id = response.json()["receipt"]["id"]

    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "1", "quantity": 1}
    )
    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "2", "quantity": 2}
    )

    response = http.get(f"/receipts/{receipt_id}/quotes")

    assert response.status_code == 200
    assert response.json()["GEL"] == 5.0


def test_should_error_on_calculate_payment_on_non_existent_receipt(
    http: TestClient,
) -> None:
    response = http.get("/receipts/invalid/quotes")

    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}


def test_should_calculate_discounted_payment(
    http: TestClient, distributor: StoreDistributor
) -> None:
    distributor.product_discount().add(
        ProductDiscountRecord(
            id="1",
            product_id="1",
            discount=0.1,
        )
    )

    response = http.post("/receipts", json={"shift_id": "1"})
    receipt_id = response.json()["receipt"]["id"]

    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "1", "quantity": 1}
    )
    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "2", "quantity": 2}
    )

    response = http.get(f"/receipts/{receipt_id}/quotes")

    assert response.status_code == 200
    assert response.json()["GEL"] == 1 * 0.9 + 2 * 2.0


def test_should_calculate_no_discount_without_campaigns(
    http: TestClient, distributor: StoreDistributor
) -> None:
    response = http.post("/receipts", json={"shift_id": "1"})
    receipt_id = response.json()["receipt"]["id"]

    response = http.get(f"/receipts/{receipt_id}/discount")

    assert response.status_code == 200
    assert response.json() == {
        "receipt_id": receipt_id,
        "discount_in_GEL": 0.0,
        "final_cost_in_GEL": 0.0,
    }

    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "1", "quantity": 1}
    )
    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "2", "quantity": 2}
    )

    response = http.get(f"/receipts/{receipt_id}/discount")

    assert response.status_code == 200
    assert response.json() == {
        "receipt_id": receipt_id,
        "discount_in_GEL": 0.0,
        "final_cost_in_GEL": 5.0,
    }


def test_should_calculate_discount_with_campaigns(
    http: TestClient, distributor: StoreDistributor
) -> None:
    distributor.product_discount().add(
        ProductDiscountRecord(
            id="1",
            product_id="1",
            discount=0.1,
        )
    )

    response = http.post("/receipts", json={"shift_id": "1"})
    receipt_id = response.json()["receipt"]["id"]

    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "2", "quantity": 2}
    )

    response = http.get(f"/receipts/{receipt_id}/discount")

    assert response.status_code == 200
    assert response.json() == {
        "receipt_id": receipt_id,
        "discount_in_GEL": 0.0,
        "final_cost_in_GEL": 2 * 2.0,
    }

    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "1", "quantity": 1}
    )

    response = http.get(f"/receipts/{receipt_id}/discount")

    assert response.status_code == 200
    assert response.json() == {
        "receipt_id": receipt_id,
        "discount_in_GEL": 5 - 1 * 0.9 - 2 * 2.0,
        "final_cost_in_GEL": 1 * 0.9 + 2 * 2.0,
    }


def test_should_error_on_discount_on_non_existent_receipt(http: TestClient) -> None:
    response = http.get("/receipts/invalid/discount")

    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}


def test_should_pay_receipt(http: TestClient, distributor: StoreDistributor) -> None:
    response = http.post("/receipts", json={"shift_id": "1"})
    receipt_id = response.json()["receipt"]["id"]

    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "1", "quantity": 1}
    )
    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "2", "quantity": 2}
    )

    response = http.post(f"/receipts/{receipt_id}/payments", json={"currency": "GEL"})

    assert response.status_code == 201
    assert response.json() == {
        "receipt": {
            "id": receipt_id,
            "open": False,
            "shift_id": "1",
            "items": [
                {
                    "id": ANY,
                    "product_id": "1",
                    "quantity": 1,
                    "price": 1.0,
                    "total": 1.0,
                },
                {
                    "id": ANY,
                    "product_id": "2",
                    "quantity": 2,
                    "price": 2.0,
                    "total": 4.0,
                },
            ],
        }
    }
    assert (
        distributor.paid_receipts()
        .filter_by_field("receipt_id", receipt_id)[0]
        .currency_name
        == "GEL"
    )


def test_should_pay_receipt_in_different_currency(
    http: TestClient, distributor: StoreDistributor
) -> None:
    response = http.post("/receipts", json={"shift_id": "1"})
    receipt_id = response.json()["receipt"]["id"]

    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "1", "quantity": 1}
    )
    response = http.post(
        f"/receipts/{receipt_id}/products", json={"product_id": "2", "quantity": 2}
    )

    response = http.post(f"/receipts/{receipt_id}/payments", json={"currency": "USD"})

    assert response.status_code == 201
    assert response.json() == {
        "receipt": {
            "id": receipt_id,
            "open": False,
            "shift_id": "1",
            "items": [
                {
                    "id": ANY,
                    "product_id": "1",
                    "quantity": 1,
                    "price": 1.0,
                    "total": 1.0,
                },
                {
                    "id": ANY,
                    "product_id": "2",
                    "quantity": 2,
                    "price": 2.0,
                    "total": 4.0,
                },
            ],
        }
    }
    assert (
        distributor.paid_receipts()
        .filter_by_field("receipt_id", receipt_id)[0]
        .currency_name
        == "USD"
    )


def test_should_error_on_close_of_non_existent_receipt(http: TestClient) -> None:
    response = http.post("/receipts/invalid/payments", json={"currency": "GEL"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Receipt not found"}
