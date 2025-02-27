from starlette.testclient import TestClient


def test_add_and_get_combo(http: TestClient) -> None:
    response = http.post(
        "/combos", json={"name": "Empty Combo", "items": [], "discount": 0.0}
    )
    assert response.status_code == 201

    combo_id = response.json()["combo"]["id"]
    response = http.get(f"/combos/{combo_id}")

    assert response.status_code == 200
    assert response.json() == {
        "combo": {"id": combo_id, "name": "Empty Combo", "items": [], "discount": 0.0}
    }


def test_add_multiple_and_get_all_combos(http: TestClient) -> None:
    response = http.post(
        "/combos", json={"name": "Empty Combo", "items": [], "discount": 0.0}
    )
    assert response.status_code == 201
    combo_id1 = response.json()["combo"]["id"]

    response = http.post(
        "/combos", json={"name": "Empty Combo", "items": [], "discount": 0.0}
    )
    assert response.status_code == 201
    combo_id2 = response.json()["combo"]["id"]

    response = http.get("/combos")

    assert response.status_code == 200
    assert response.json() == {
        "combos": [
            {"id": combo_id1, "name": "Empty Combo", "items": [], "discount": 0.0},
            {"id": combo_id2, "name": "Empty Combo", "items": [], "discount": 0.0},
        ]
    }


def test_add_and_remove_combo(http: TestClient) -> None:
    response = http.post(
        "/combos", json={"name": "Empty Combo", "items": [], "discount": 0.0}
    )
    assert response.status_code == 201
    combo_id = response.json()["combo"]["id"]

    response = http.patch(f"/combos/{combo_id}")
    assert response.status_code == 200

    response = http.get(f"/combos/{combo_id}")
    assert response.status_code == 404
