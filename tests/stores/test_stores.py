from fastapi.testclient import TestClient

from wapang.app.users.models import User

def test_create_store(
    client: TestClient,
    access_token: str,
    store_create_request: dict,
):
    res = client.post("/api/stores", json=store_create_request, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 201
    res_json = res.json()
    assert res_json["id"] is not None
    assert res_json["store_name"] == store_create_request["store_name"]
    assert res_json["address"] == store_create_request["address"]
    assert res_json["email"] == store_create_request["email"]
    assert res_json["phone_number"] == store_create_request["phone_number"]
    assert res_json["delivery_fee"] == store_create_request["delivery_fee"]

def test_create_store_with_missing_fields(
    client: TestClient,
    access_token: str,
    store_create_request: dict,
):
    req = store_create_request
    del req["store_name"]

    res = client.post("/api/stores", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_002"
    assert res.json()["error_msg"] == "MISSING REQUIRED FIELDS"

def test_create_store_with_short_store_name(
    client: TestClient,
    access_token: str,
    store_create_request: dict,
):
    req = store_create_request
    req["store_name"] = "A"

    res = client.post("/api/stores", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"

def test_create_store_with_long_store_name(
    client: TestClient,
    access_token: str,
    store_create_request: dict,
):
    req = store_create_request
    req["store_name"] = "A" * 21

    res = client.post("/api/stores", json=req, headers={"Authorization": f"Bearer {access_token}"})

    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"


def test_create_store_with_long_address(
    client: TestClient,
    access_token: str,
    store_create_request: dict,
):
    req = store_create_request
    req["address"] = "A" * 101

    res = client.post("/api/stores", json=req, headers={"Authorization": f"Bearer {access_token}"})

    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"

def test_create_store_with_invalid_delivery_fee(
    client: TestClient,
    access_token: str,
    store_create_request: dict,
):
    req = store_create_request
    req["delivery_fee"] = -100

    res = client.post("/api/stores", json=req, headers={"Authorization": f"Bearer {access_token}"})

    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"


def test_create_store_store_name_conflict(
    client: TestClient,
    store: dict,
    another_user_access_token: str,
):
    req = {
        "store_name": "My Store",
        "address": "2, Gwanak-ro, Gwanak-gu, Seoul, Republic of Korea",
        "email": "spring@wafflestudio.com",
        "phone_number": "010-1111-2222",
        "delivery_fee": 4000
    }

    res = client.post("/api/stores", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})

    assert res.status_code == 409
    res_json = res.json()
    assert res_json["error_code"] == "ERR_009"
    assert res_json["error_msg"] == "STORE INFO CONFLICT"

def test_create_store_email_conflict(
    client: TestClient,
    store: dict,
    another_user_access_token: str,
):
    req = {
        "store_name": "Your Store",
        "address": "2, Gwanak-ro, Gwanak-gu, Seoul, Republic of Korea",
        "email": "fastapi@wafflestudio.com",
        "phone_number": "010-1111-2222",
        "delivery_fee": 4000
    }

    res = client.post("/api/stores", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 409
    res_json = res.json()
    assert res_json["error_code"] == "ERR_009"
    assert res_json["error_msg"] == "STORE INFO CONFLICT"

def test_create_store_phone_number_conflict(
    client: TestClient,
    store: dict,
    another_user_access_token: str,
):
    req = {
        "store_name": "Your Store",
        "address": "2, Gwanak-ro, Gwanak-gu, Seoul, Republic of Korea",
        "email": "spring@wafflestudio.com",
        "phone_number": "010-1234-5678",
        "delivery_fee": 4000
    }
    res = client.post("/api/stores", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 409
    res_json = res.json()
    assert res_json["error_code"] == "ERR_009"
    assert res_json["error_msg"] == "STORE INFO CONFLICT"

def test_create_store_already_exists(
    client: TestClient,
    access_token: str,
    store: dict,
):
    req = {
        "store_name": "Another Store",
        "address": "2, Gwanak-ro, Gwanak-gu, Seoul, Republic of Korea",
        "email": "spring@wafflestudio.com",
        "phone_number": "010-1111-2222",
        "delivery_fee": 4000
    }

    res = client.post("/api/stores", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 409
    res_json = res.json()
    assert res_json["error_code"] == "ERR_008"
    assert res_json["error_msg"] == "STORE ALREADY EXISTS"

def test_patch_store(
    client: TestClient,
    access_token: str,
    store: dict,
):
    store_id = store["id"]
    req = {
        "store_name": "Updated Store",
        "address": "Updated Address",
        "email": "updated@wafflestudio.com",
        "phone_number": "010-9999-8888",
        "delivery_fee": 5000
    }

    res = client.patch(f"/api/stores/{store_id}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["id"] == store_id
    assert res_json["store_name"] == req["store_name"]
    assert res_json["address"] == req["address"]
    assert res_json["email"] == req["email"]
    assert res_json["phone_number"] == req["phone_number"]
    assert res_json["delivery_fee"] == req["delivery_fee"]

def test_patch_store_with_long_name(
    client: TestClient,
    access_token: str,
    store: dict,
):
    store_id = store["id"]
    req = {
        "store_name": "A" * 21,
        "address": "Updated Address",
        "email": "updated@wafflestudio.com",
        "phone_number": "010-9999-8888",
        "delivery_fee": 5000
    }

    res = client.patch(f"/api/stores/{store_id}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"

def test_patch_store_with_long_address(
    client: TestClient,
    access_token: str,
    store: dict,
):
    store_id = store["id"]
    req = {
        "store_name": "Updated Store",
        "address": "A" * 101,
        "email": "updated@wafflestudio.com",
        "phone_number": "010-9999-8888",
        "delivery_fee": 5000
    }

    res = client.patch(f"/api/stores/{store_id}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"

def test_patch_store_with_invalid_delivery_fee(
    client: TestClient,
    access_token: str,
    store: dict,
):
    store_id = store["id"]
    req = {
        "store_name": "Updated Store",
        "address": "Updated Address",
        "email": "updated@wafflestudio.com",
        "phone_number": "010-9999-8888",
        "delivery_fee": -100
    }

    res = client.patch(f"/api/stores/{store_id}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"

def test_patch_store_not_found(
    client: TestClient,
    access_token: str,
):
    store_id = 99999  # Non-existent store ID
    req = {
        "store_name": "Updated Store",
        "address": "Updated Address",
        "email": "updated@wafflestudio.com",
        "phone_number": "010-9999-8888",
        "delivery_fee": 5000
    }

    res = client.patch(f"/api/stores/{store_id}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 404
    res_json = res.json()
    assert res_json["error_code"] == "ERR_010"
    assert res_json["error_msg"] == "STORE NOT FOUND"

def test_patch_store_not_owned(
    client: TestClient,
    store: dict,
    another_user_access_token: str,
):
    req = {
        "store_name": "Updated Store",
        "address": "Updated Address",
        "email": "updated@wafflestudio.com",
        "phone_number": "010-9999-8888",
        "delivery_fee": 5000
    }
    store_id = store["id"]
    res = client.patch(f"/api/stores/{store_id}", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 403
    res_json = res.json()
    assert res_json["error_code"] == "ERR_011"
    assert res_json["error_msg"] == "NO STORE OWNED"

def test_patch_store_unauthorized(
    client: TestClient,
    store: dict,
    store_2: dict,
    another_user_access_token: str,
):
    store_id = store["id"]
    req = {
        "store_name": "Updated Store",
        "address": "Updated Address",
        "email": "updated@wafflestudio.com",
        "phone_number": "010-9999-8888",
        "delivery_fee": 5000
    }

    res = client.patch(f"/api/stores/{store_id}", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 403
    res_json = res.json()
    assert res_json["error_code"] == "ERR_012"
    assert res_json["error_msg"] == "NOT YOUR STORE"

def test_patch_store_store_name_conflict(
    client: TestClient,
    store: dict,
    store_2: dict,
    another_user_access_token: str,
):
    req = {
        "store_name": store["store_name"],
    }

    res = client.patch(f"/api/stores/{store_2['id']}", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 409
    res_json = res.json()
    assert res_json["error_code"] == "ERR_009"
    assert res_json["error_msg"] == "STORE INFO CONFLICT"

def test_patch_store_email_conflict(
    client: TestClient,
    store: dict,
    store_2: dict,
    another_user_access_token: str,
):
    another_store_id = store_2["id"]
    req = {
        "email": store["email"],
    }
    res = client.patch(f"/api/stores/{another_store_id}", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 409
    res_json = res.json()
    assert res_json["error_code"] == "ERR_009"
    assert res_json["error_msg"] == "STORE INFO CONFLICT"

def test_patch_store_phone_number_conflict(
    client: TestClient,
    store: dict,
    store_2: dict,
    another_user_access_token: str,
):
    another_store_id = store_2["id"]
    req = {
        "phone_number": store["phone_number"],
    }
    res = client.patch(f"/api/stores/{another_store_id}", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 409
    res_json = res.json()
    assert res_json["error_code"] == "ERR_009"
    assert res_json["error_msg"] == "STORE INFO CONFLICT"

def test_get_store(
    client: TestClient,
    store: dict,
):
    store_id = store["id"]

    res = client.get(f"/api/stores/{store_id}")
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["id"] == store_id
    assert res_json["store_name"] == store["store_name"]
    assert res_json["address"] == store["address"]
    assert res_json["email"] == store["email"]
    assert res_json["phone_number"] == store["phone_number"]
    assert res_json["delivery_fee"] == store["delivery_fee"]

def test_get_store_not_found(
    client: TestClient,
):
    store_id = 99999

    res = client.get(f"/api/stores/{store_id}")
    assert res.status_code == 404
    res_json = res.json()
    assert res_json["error_code"] == "ERR_010"
    assert res_json["error_msg"] == "STORE NOT FOUND"