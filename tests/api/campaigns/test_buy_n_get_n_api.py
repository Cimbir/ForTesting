from starlette.testclient import TestClient

from tests.api.utils import create_n_products


def test_add_and_get_buy_n_get_n(http: TestClient) -> None:
    product_ids = create_n_products(http, 2)
    buy_product_id, get_product_id = product_ids

    response = http.post(
        "/buy_n_get_n",
        json={
            "buy_product_id": buy_product_id,
            "buy_product_n": 2,
            "get_product_id": get_product_id,
            "get_product_n": 1,
        },
    )
    assert response.status_code == 201

    buy_n_get_n_id = response.json()["buy_n_get_n"]["id"]
    response = http.get(f"/buy_n_get_n/{buy_n_get_n_id}")

    assert response.status_code == 200
    assert response.json() == {
        "buy_n_get_n": {
            "id": buy_n_get_n_id,
            "buy_product_id": buy_product_id,
            "buy_product_n": 2,
            "get_product_id": get_product_id,
            "get_product_n": 1,
        }
    }


def test_add_multiple_and_get_all_buy_n_get_ns(http: TestClient) -> None:
    product_ids = create_n_products(http, 4)
    buy_product_id1, get_product_id1, buy_product_id2, get_product_id2 = product_ids

    response = http.post(
        "/buy_n_get_n",
        json={
            "buy_product_id": buy_product_id1,
            "buy_product_n": 2,
            "get_product_id": get_product_id1,
            "get_product_n": 1,
        },
    )
    assert response.status_code == 201
    buy_n_get_n_id1 = response.json()["buy_n_get_n"]["id"]

    response = http.post(
        "/buy_n_get_n",
        json={
            "buy_product_id": buy_product_id2,
            "buy_product_n": 3,
            "get_product_id": get_product_id2,
            "get_product_n": 2,
        },
    )
    assert response.status_code == 201
    buy_n_get_n_id2 = response.json()["buy_n_get_n"]["id"]

    response = http.get("/buy_n_get_n")

    assert response.status_code == 200
    assert response.json() == {
        "buy_n_get_ns": [
            {
                "id": buy_n_get_n_id1,
                "buy_product_id": buy_product_id1,
                "buy_product_n": 2,
                "get_product_id": get_product_id1,
                "get_product_n": 1,
            },
            {
                "id": buy_n_get_n_id2,
                "buy_product_id": buy_product_id2,
                "buy_product_n": 3,
                "get_product_id": get_product_id2,
                "get_product_n": 2,
            },
        ]
    }


def test_add_and_remove_buy_n_get_n(http: TestClient) -> None:
    product_ids = create_n_products(http, 2)
    buy_product_id, get_product_id = product_ids

    response = http.post(
        "/buy_n_get_n",
        json={
            "buy_product_id": buy_product_id,
            "buy_product_n": 2,
            "get_product_id": get_product_id,
            "get_product_n": 1,
        },
    )
    assert response.status_code == 201
    buy_n_get_n_id = response.json()["buy_n_get_n"]["id"]

    response = http.patch(f"/buy_n_get_n/{buy_n_get_n_id}")
    assert response.status_code == 200

    response = http.get(f"/buy_n_get_n/{buy_n_get_n_id}")
    assert response.status_code == 404
