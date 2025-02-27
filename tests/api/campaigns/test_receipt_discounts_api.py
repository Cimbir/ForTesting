from starlette.testclient import TestClient


def test_add_and_get_receipt_discount(http: TestClient) -> None:
    response = http.post(
        "/receipt_discounts", json={"minimum_total": 100.0, "discount": 10.0}
    )
    assert response.status_code == 201

    receipt_discount_id = response.json()["receipt_discount"]["id"]
    response = http.get(f"/receipt_discounts/{receipt_discount_id}")

    assert response.status_code == 200
    assert response.json() == {
        "receipt_discount": {
            "id": receipt_discount_id,
            "minimum_total": 100.0,
            "discount": 10.0,
        }
    }


def test_add_multiple_and_get_all_receipt_discounts(http: TestClient) -> None:
    response = http.post(
        "/receipt_discounts", json={"minimum_total": 100.0, "discount": 10.0}
    )
    assert response.status_code == 201
    receipt_discount_id1 = response.json()["receipt_discount"]["id"]

    response = http.post(
        "/receipt_discounts", json={"minimum_total": 200.0, "discount": 20.0}
    )
    assert response.status_code == 201
    receipt_discount_id2 = response.json()["receipt_discount"]["id"]

    response = http.get("/receipt_discounts")

    assert response.status_code == 200
    assert response.json() == {
        "receipt_discounts": [
            {"id": receipt_discount_id1, "minimum_total": 100.0, "discount": 10.0},
            {"id": receipt_discount_id2, "minimum_total": 200.0, "discount": 20.0},
        ]
    }


def test_add_and_remove_receipt_discount(http: TestClient) -> None:
    response = http.post(
        "/receipt_discounts", json={"minimum_total": 100.0, "discount": 10.0}
    )
    assert response.status_code == 201
    receipt_discount_id = response.json()["receipt_discount"]["id"]

    response = http.patch(f"/receipt_discounts/{receipt_discount_id}")
    assert response.status_code == 200

    response = http.get(f"/receipt_discounts/{receipt_discount_id}")
    assert response.status_code == 404