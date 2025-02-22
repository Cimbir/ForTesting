from starlette.testclient import TestClient


def test_should_return_no_products_when_no_products(http: TestClient) -> None:
    response = http.get("/products")

    assert response.status_code == 200
    assert response.json() == {"products": []}
