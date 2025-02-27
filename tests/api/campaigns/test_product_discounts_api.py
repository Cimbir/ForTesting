from starlette.testclient import TestClient

from tests.api.utils import create_n_products


def test_add_and_get_product_discount(http: TestClient) -> None:
    product_ids = create_n_products(http, 1)
    product_id1 = product_ids[0]

    response = http.post(
        "/product_discounts",
        json={"product_id": product_id1, "discount": 0.1},
    )
    assert response.status_code == 201

    product_discount_id = response.json()["product_discount"]["id"]
    response = http.get(f"/product_discounts/{product_discount_id}")

    assert response.status_code == 200
    assert response.json() == {
        "product_discount": {
            "id": product_discount_id,
            "product_id": product_id1,
            "discount": 0.1,
        }
    }


def test_add_multiple_and_get_all_product_discounts(http: TestClient) -> None:
    product_ids = create_n_products(http, 2)
    product_id1, product_id2 = product_ids

    response = http.post(
        "/product_discounts",
        json={"product_id": product_id1, "discount": 0.1},
    )
    assert response.status_code == 201
    product_discount_id1 = response.json()["product_discount"]["id"]

    response = http.post(
        "/product_discounts",
        json={"product_id": product_id2, "discount": 0.2},
    )
    assert response.status_code == 201
    product_discount_id2 = response.json()["product_discount"]["id"]

    response = http.get("/product_discounts")

    assert response.status_code == 200
    assert response.json() == {
        "product_discounts": [
            {"id": product_discount_id1, "product_id": product_id1, "discount": 0.1},
            {"id": product_discount_id2, "product_id": product_id2, "discount": 0.2},
        ]
    }


def test_add_and_remove_product_discount(http: TestClient) -> None:
    product_ids = create_n_products(http, 1)
    product_id1 = product_ids[0]

    response = http.post(
        "/product_discounts",
        json={"product_id": product_id1, "discount": 0.1},
    )
    assert response.status_code == 201
    product_discount_id = response.json()["product_discount"]["id"]

    response = http.patch(f"/product_discounts/{product_discount_id}")
    assert response.status_code == 200

    response = http.get(f"/product_discounts/{product_discount_id}")
    assert response.status_code == 404
