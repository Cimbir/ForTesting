from starlette.testclient import TestClient

def create_n_products(http: TestClient, n: int) -> list:
    product_ids = []
    for i in range(n):
        response = http.post("/products", json={"name": f"test{i+1}", "price": float(i+1)})
        assert response.status_code == 201
        product_ids.append(response.json()["product"]["id"])
    return product_ids

def test_add_and_get_combo(http: TestClient) -> None:
    response = http.post("/campaigns/combos", json={"name": "Empty Combo", "items": [], "discount": 0.0})
    assert response.status_code == 201

    combo_id = response.json()["combo"]["id"]
    response = http.get(f"/campaigns/combos/{combo_id}")

    assert response.status_code == 200
    assert response.json() == {"combo": {"id": combo_id, "name": "Empty Combo", "items": [], "discount": 0.0}}

def test_add_multiple_and_get_all_combos(http: TestClient) -> None:
    response = http.post("/campaigns/combos", json={"name": "Empty Combo", "items": [], "discount": 0.0})
    assert response.status_code == 201
    combo_id1 = response.json()["combo"]["id"]

    response = http.post("/campaigns/combos", json={"name": "Empty Combo", "items": [], "discount": 0.0})
    assert response.status_code == 201
    combo_id2 = response.json()["combo"]["id"]

    response = http.get("/campaigns/combos")

    assert response.status_code == 200
    assert response.json() == {
        "combos": [
            {"id": combo_id1, "name": "Empty Combo", "items": [], "discount": 0.0},
            {"id": combo_id2, "name": "Empty Combo", "items": [], "discount": 0.0},
        ]
    }

def test_add_and_remove_combo(http: TestClient) -> None:
    response = http.post("/campaigns/combos", json={"name": "Empty Combo", "items": [], "discount": 0.0})
    assert response.status_code == 201
    combo_id = response.json()["combo"]["id"]

    response = http.patch(f"/campaigns/combos/{combo_id}")
    assert response.status_code == 200

    response = http.get(f"/campaigns/combos/{combo_id}")
    assert response.status_code == 404


def test_add_and_get_product_discount(http: TestClient) -> None:
    product_ids = create_n_products(http, 1)
    product_id1 = product_ids[0]

    response = http.post("/campaigns/product_discounts", json={"product_id": product_id1, "discount": 0.1})
    assert response.status_code == 201

    product_discount_id = response.json()["product_discount"]["id"]
    response = http.get(f"/campaigns/product_discounts/{product_discount_id}")

    assert response.status_code == 200
    assert response.json() == {"product_discount": {"id": product_discount_id,
                                                    "product_id": product_id1,
                                                    "discount": 0.1}}

def test_add_multiple_and_get_all_product_discounts(http: TestClient) -> None:
    product_ids = create_n_products(http, 2)
    product_id1, product_id2 = product_ids

    response = http.post("/campaigns/product_discounts", json={"product_id": product_id1, "discount": 0.1})
    assert response.status_code == 201
    product_discount_id1 = response.json()["product_discount"]["id"]

    response = http.post("/campaigns/product_discounts", json={"product_id": product_id2, "discount": 0.2})
    assert response.status_code == 201
    product_discount_id2 = response.json()["product_discount"]["id"]

    response = http.get("/campaigns/product_discounts")

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

    response = http.post("/campaigns/product_discounts",
                         json={"product_id": product_id1, "discount": 0.1})
    assert response.status_code == 201
    product_discount_id = response.json()["product_discount"]["id"]

    response = http.patch(f"/campaigns/product_discounts/{product_discount_id}")
    assert response.status_code == 200

    response = http.get(f"/campaigns/product_discounts/{product_discount_id}")
    assert response.status_code == 404

def test_add_and_get_buy_n_get_n(http: TestClient) -> None:
    product_ids = create_n_products(http, 2)
    buy_product_id, get_product_id = product_ids

    response = http.post("/campaigns/buy_n_get_n",
                         json={"buy_product_id": buy_product_id, "buy_product_n": 2,
                               "get_product_id": get_product_id, "get_product_n": 1})
    assert response.status_code == 201

    buy_n_get_n_id = response.json()["buy_n_get_n"]["id"]
    response = http.get(f"/campaigns/buy_n_get_n/{buy_n_get_n_id}")

    assert response.status_code == 200
    assert response.json() == {"buy_n_get_n": {"id": buy_n_get_n_id,
                                              "buy_product_id": buy_product_id,
                                              "buy_product_n": 2,
                                              "get_product_id": get_product_id,
                                              "get_product_n": 1}}

def test_add_multiple_and_get_all_buy_n_get_ns(http: TestClient) -> None:
    product_ids = create_n_products(http, 4)
    buy_product_id1, get_product_id1, buy_product_id2, get_product_id2 = product_ids

    response = http.post("/campaigns/buy_n_get_n",
                         json={"buy_product_id": buy_product_id1, "buy_product_n": 2,
                               "get_product_id": get_product_id1, "get_product_n": 1})
    assert response.status_code == 201
    buy_n_get_n_id1 = response.json()["buy_n_get_n"]["id"]

    response = http.post("/campaigns/buy_n_get_n",
                         json={"buy_product_id": buy_product_id2, "buy_product_n": 3,
                               "get_product_id": get_product_id2, "get_product_n": 2})
    assert response.status_code == 201
    buy_n_get_n_id2 = response.json()["buy_n_get_n"]["id"]

    response = http.get("/campaigns/buy_n_get_n")

    assert response.status_code == 200
    assert response.json() == {
        "buy_n_get_ns": [
            {"id": buy_n_get_n_id1, "buy_product_id": buy_product_id1, "buy_product_n": 2,
             "get_product_id": get_product_id1, "get_product_n": 1},
            {"id": buy_n_get_n_id2, "buy_product_id": buy_product_id2, "buy_product_n": 3,
             "get_product_id": get_product_id2, "get_product_n": 2},
        ]
    }

def test_add_and_remove_buy_n_get_n(http: TestClient) -> None:
    product_ids = create_n_products(http, 2)
    buy_product_id, get_product_id = product_ids

    response = http.post("/campaigns/buy_n_get_n",
                         json={"buy_product_id": buy_product_id, "buy_product_n": 2,
                               "get_product_id": get_product_id, "get_product_n": 1})
    assert response.status_code == 201
    buy_n_get_n_id = response.json()["buy_n_get_n"]["id"]

    response = http.patch(f"/campaigns/buy_n_get_n/{buy_n_get_n_id}")
    assert response.status_code == 200

    response = http.get(f"/campaigns/buy_n_get_n/{buy_n_get_n_id}")
    assert response.status_code == 404

def test_add_and_get_receipt_discount(http: TestClient) -> None:
    response = http.post("/campaigns/receipt_discounts", json={"minimum_total": 100.0, "discount": 10.0})
    assert response.status_code == 201

    receipt_discount_id = response.json()["receipt_discount"]["id"]
    response = http.get(f"/campaigns/receipt_discounts/{receipt_discount_id}")

    assert response.status_code == 200
    assert response.json() == {"receipt_discount": {"id": receipt_discount_id,
                                                   "minimum_total": 100.0,
                                                   "discount": 10.0}}

def test_add_multiple_and_get_all_receipt_discounts(http: TestClient) -> None:
    response = http.post("/campaigns/receipt_discounts", json={"minimum_total": 100.0, "discount": 10.0})
    assert response.status_code == 201
    receipt_discount_id1 = response.json()["receipt_discount"]["id"]

    response = http.post("/campaigns/receipt_discounts", json={"minimum_total": 200.0, "discount": 20.0})
    assert response.status_code == 201
    receipt_discount_id2 = response.json()["receipt_discount"]["id"]

    response = http.get("/campaigns/receipt_discounts")

    assert response.status_code == 200
    assert response.json() == {
        "receipt_discounts": [
            {"id": receipt_discount_id1, "minimum_total": 100.0, "discount": 10.0},
            {"id": receipt_discount_id2, "minimum_total": 200.0, "discount": 20.0},
        ]
    }

def test_add_and_remove_receipt_discount(http: TestClient) -> None:
    response = http.post("/campaigns/receipt_discounts", json={"minimum_total": 100.0, "discount": 10.0})
    assert response.status_code == 201
    receipt_discount_id = response.json()["receipt_discount"]["id"]

    response = http.patch(f"/campaigns/receipt_discounts/{receipt_discount_id}")
    assert response.status_code == 200

    response = http.get(f"/campaigns/receipt_discounts/{receipt_discount_id}")
    assert response.status_code == 404