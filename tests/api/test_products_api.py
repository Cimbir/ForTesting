from starlette.testclient import TestClient


def test_should_return_no_products_when_no_products(http: TestClient) -> None:
    response = http.get("/products")

    assert response.status_code == 200
    assert response.json() == {"products": []}

def test_add_and_get_by_id(http: TestClient) -> None:
    response = http.post("/products", json={"name": "test", "price": 1.0})

    assert response.status_code == 201
    product_id = response.json()["product"]["id"]

    response = http.get(f"/products/{product_id}")

    assert response.status_code == 200
    assert response.json() == {"product": {"id": product_id, "name": "test", "price": 1.0}}

def test_add_multiple_and_get_all(http: TestClient) -> None:
    response = http.post("/products", json={"name": "test1", "price": 1.0})
    assert response.status_code == 201
    product_id1 = response.json()["product"]["id"]

    response = http.post("/products", json={"name": "test2", "price": 2.0})
    assert response.status_code == 201
    product_id2 = response.json()["product"]["id"]

    response = http.get("/products")

    assert response.status_code == 200
    assert response.json() == {
        "products": [
            {"id": product_id1, "name": "test1", "price": 1.0},
            {"id": product_id2, "name": "test2", "price": 2.0},
        ]
    }

def test_update_and_get_by_id(http: TestClient) -> None:
    response = http.post("/products", json={"name": "test", "price": 1.0})
    assert response.status_code == 201
    product_id = response.json()["product"]["id"]

    response = http.patch(f"/products/{product_id}", json={"name": "new name", "price": 2.0})

    assert response.status_code == 200
    assert response.json() == {"product": {"id": product_id, "name": "new name", "price": 2.0}}