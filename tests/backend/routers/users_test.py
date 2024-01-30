from fastapi.testclient import TestClient

from backend.main import app


def test_get_all_users():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200
    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])


def test_create_user():
    client = TestClient(app)
    create_params = {
        "id": "333",
    }
    response = client.post("/users", json = create_params)
    assert response.status_code == 200
    user = response.json()["user"]
    assert "created_at" in user
    assert user["id"] == "333"

def test_create_existing_user():
    client = TestClient(app)
    create_params = {
        "id": "terminator",
    }
    response = client.post("/users", json = create_params)
    assert response.status_code == 422
    assert response.json() == {
            "detail": {
                "type": "duplicate_entity",
                "entity_name": "User",
                "entity_id": "terminator",
            },
        }

def test_get_user():
    user_id = "bomb20"
    client = TestClient(app)
    response = client.get(f"/users/{user_id}")
    user = response.json()["user"]
    assert response.status_code == 200
    assert response.json() == {
            "user": {
            "id": "bomb20",
            "created_at": "2022-03-21T08:30:02"
        },
        }


def test_get_invalid_user():
    user_id = "12123235446654"
    client = TestClient(app)
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json() == {
            "detail": {
                "type": "entity_not_found",
                "entity_name": "User",
                "entity_id": "12123235446654",
            },
        }
    
def test_get_user_chats():
    user_id = "reese"
    client = TestClient(app)
    response = client.get(f"/users/{user_id}/chats")
    assert response.status_code == 200
    assert response.json() == {
            "meta": {
                "count": 1
            },
            "chats": [
                {
                    "id": "660c7a6bc1324e4488cafabc59529c93",
                    "name": "terminators",
                    "user_ids": [
                        "reese",
                        "sarah"
                    ],
                    "owner_id": "reese",
                    "created_at": "2023-04-12T20:11:21"
                }
            ]
        }
def test_get_invalid_user_chats():
    user_id = "4356457"
    client = TestClient(app)
    response = client.get(f"/users/{user_id}/chats")
    assert response.status_code == 404
    assert response.json() == {
            "detail": {
                "type": "entity_not_found",
                "entity_name": "User",
                "entity_id": "4356457",
            },
        }

