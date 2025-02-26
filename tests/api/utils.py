from starlette.testclient import TestClient


def create_n_products(http: TestClient, n: int) -> list:
    product_ids = []
    for i in range(n):
        response = http.post(
            "/products", json={"name": f"test{i + 1}", "price": float(i + 1)}
        )
        assert response.status_code == 201
        product_ids.append(response.json()["product"]["id"])
    return product_ids