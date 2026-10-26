from fastapi.testclient import TestClient
import pytest
import random


def test_create_order(
    client: TestClient,
    access_token: str,
    order_items: list[dict]
):
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
    assert res_json["status"] == "ORDERED"
    details = res_json["details"]
    stores = set()
    for item in order_items:
        stores.add(item["store_id"])
    assert len(details) == len(stores)
    for detail in details:
        assert detail["store_id"] in stores
        for item in detail["items"]:
            matched = None
            for req_item in req:
                if req_item["item_id"] == item["item_id"]:
                    matched = req_item
                    break
            assert matched is not None
            assert item["quantity"] == matched["quantity"]
            for order_item in order_items:
                if order_item["id"] == item["item_id"]:
                    assert item["item_name"] == order_item["item_name"]
                    assert item["price"] == order_item["price"]
                    break
    
    total_price = 0
    for detail in details:
        store_total_price = 0
        for item in detail["items"]:
            store_total_price += item["price"] * item["quantity"]
        store_total_price += detail["delivery_fee"]
        assert detail["store_total_price"] == store_total_price
        total_price += store_total_price
    assert res_json["total_price"] == total_price

def test_create_order_with_nonexistent_item(
    client: TestClient,
    access_token: str,
    order_items: list[dict]
):
    req = []
    for item in order_items:
        req.append({
            "item_id": item["id"],
            "quantity": random.randint(1, item["stock"])
        })
    req.append({
        "item_id": "test_nonexistent_item_id",
        "quantity": 1
    })

    res = client.post("/api/orders", json={"items": req}, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 404
    res_json = res.json()
    assert res_json["error_code"] == "ERR_013"
    assert res_json["error_msg"] == "ITEM NOT FOUND"

def test_create_order_with_not_enough_stock(
    client: TestClient,
    access_token: str,
    item: dict,
):
    req = [{
        "item_id": item["id"],
        "quantity": item["stock"] + 10
    }]

    res = client.post("/api/orders", json={"items": req}, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 409
    res_json = res.json()
    assert res_json["error_code"] == "ERR_017"
    assert res_json["error_msg"] == "NOT ENOUGH STOCK"

def test_create_order_with_no_items(
    client: TestClient,
    access_token: str,
):
    req = []

    res = client.post("/api/orders", json={"items": req}, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 422
    res_json = res.json()
    assert res_json["error_code"] == "ERR_018"
    assert res_json["error_msg"] == "EMPTY ITEM LIST"

def test_get_order(
    client: TestClient,
    access_token: str,
    order: dict,
):
    order_id = order["order_id"]
    res = client.get(f"/api/orders/{order_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    res_json = res.json()
    assert res_json == order

def test_get_order_with_invalid_order_id(
    client: TestClient,
    access_token: str,
    order: dict,
):
    order_id = "invalid_order_id"
    res = client.get(f"/api/orders/{order_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 404
    res_json = res.json()
    assert res_json["error_code"] == "ERR_019"
    assert res_json["error_msg"] == "ORDER NOT FOUND"

def test_get_order_of_another_user(
    client: TestClient,
    access_token: str,
    another_user_access_token: str,
    order: dict,
):
    order_id = order["order_id"]
    res = client.get(f"/api/orders/{order_id}", headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 403
    res_json = res.json()
    assert res_json["error_code"] == "ERR_020"
    assert res_json["error_msg"] == "NOT YOUR ORDER"

def test_update_order_status(
    client: TestClient,
    access_token: str,
    order: dict,
):
    order_id = order["order_id"]
    req = {
        "status": "CANCELED"
    }
    res = client.patch(f"/api/orders/{order_id}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 204
    assert res.content == b""

    res = client.get(f"/api/orders/{order_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["status"] == "CANCELED"

def test_update_order_status_already_canceled(
    client: TestClient,
    access_token: str,
    order: dict,
):
    order_id = order["order_id"]
    req = {
        "status": "CANCELED"
    }
    res = client.patch(f"/api/orders/{order_id}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 204
    assert res.content == b""

    res = client.patch(f"/api/orders/{order_id}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 409
    res_json = res.json()
    assert res_json["error_code"] == "ERR_021"
    assert res_json["error_msg"] == "INVALID ORDER STATUS"

def test_update_order_status_of_another_user(
    client: TestClient,
    access_token: str,
    another_user_access_token: str,
    order: dict,
):
    order_id = order["order_id"]
    req = {
        "status": "CANCELED"
    }
    res = client.patch(f"/api/orders/{order_id}", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 403
    res_json = res.json()
    assert res_json["error_code"] == "ERR_020"
    assert res_json["error_msg"] == "NOT YOUR ORDER"

def test_update_order_status_with_invalid_order_id(
    client: TestClient,
    access_token: str,
    order: dict,
):
    order_id = "invalid_order_id"
    req = {
        "status": "CANCELED"
    }
    res = client.patch(f"/api/orders/{order_id}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 404
    res_json = res.json()
    assert res_json["error_code"] == "ERR_019"
    assert res_json["error_msg"] == "ORDER NOT FOUND"

def test_get_orders_by_user(
    client: TestClient,
    access_token: str,
    order: dict,
):
    res = client.get("/api/users/me/orders", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    res_json = res.json()
    assert isinstance(res_json, list)
    assert len(res_json) >= 1