from fastapi.testclient import TestClient
import pytest
import random

@pytest.fixture
def order_items(
    client: TestClient,
    access_token: str,
    another_user_access_token: str,
    store: dict,
    store_2: dict,
) -> list[dict]:
    item_list = []
    for i in range(3):
        req = {
            "item_name": f"초콜릿_{i}",
            "price": 5000 + i * 2000,
            "stock": 10 + i * 5
        }
        res = client.post("/api/items", json=req, headers={"Authorization": f"Bearer {access_token}"})
        res_json = res.json()
        assert res.status_code == 201
        assert res_json["item_name"] == req["item_name"]
        assert res_json["price"] == req["price"]
        assert res_json["stock"] == req["stock"]
        res_json["store_id"] = store["id"]
        item_list.append(res_json)
    
    for i in range(2):
        req = {
            "item_name": f"사탕_{i}",
            "price": 3000 + i * 1000,
            "stock": 20 + i * 10
        }
        res = client.post("/api/items", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
        res_json = res.json()
        assert res.status_code == 201
        assert res_json["item_name"] == req["item_name"]
        assert res_json["price"] == req["price"]
        assert res_json["stock"] == req["stock"]
        res_json["store_id"] = store_2["id"]
        item_list.append(res_json)

    return item_list

@pytest.fixture
def order(client: TestClient, access_token: str, order_items: list[dict]) -> dict:
    req = []
    for item in order_items:
        req.append({
            "item_id": item["id"],
            "quantity": random.randint(1, item["stock"])
        })

    res = client.post("/api/orders", json={"items": req}, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 201
    res_json = res.json()
    assert res_json["order_id"] is not None
    return res_json