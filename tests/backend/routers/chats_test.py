from fastapi.testclient import TestClient

from backend.main import app

def test_get_all_chats():
    client = TestClient(app)
    response = client.get("/chats")
    assert response.status_code == 200
    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda chat: chat["name"])


def test_get_chat():
    chat_id = "660c7a6bc1324e4488cafabc59529c93"
    client = TestClient(app)
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    assert response.json() == {
            "chat": {
                "id": "660c7a6bc1324e4488cafabc59529c93",
                "name": "terminators",
                "user_ids": [
                    "reese",
                    "sarah"
                ],
                "owner_id": "reese",
                "created_at": "2023-04-12T20:11:21"
            }
        }

def test_get_invalid_chat():
    chat_id = "12123235446654"
    client = TestClient(app)
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
            "detail": {
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": "12123235446654",
            },
        }
    
def test_update_chat():
    chat_id = "6215e6864e884132baa01f7f972400e2"
    update_params = {"name": "yessir"}
    expected_chat = {
            "id": "6215e6864e884132baa01f7f972400e2",
            "name": "yessir",
            "user_ids": [
                "sarah",
                "terminator"
            ],
            "owner_id": "sarah",
            "created_at": "2023-07-08T18:46:47"
    }
    client = TestClient(app)
    response = client.put(f"/chats/{chat_id}", json=update_params)
    assert response.status_code == 200
    assert response.json() == {"chat": expected_chat}

    # test that the update is persisted
    response = client.get(f"/chats/{chat_id}")
    assert response.status_code == 200
    assert response.json() == {"chat": expected_chat}


def test_update_invalid_chat():
    chat_id = "1"
    update_params = {"name": "yessir"}
    client = TestClient(app)
    response = client.put(f"/chats/{chat_id}", json=update_params)
    assert response.status_code == 404
    assert response.json() == {
            "detail": {
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": "1",
            },
        }
    

def test_delete_chat():
    chat_id = "734eeb9ddaec43b2ab6e289a0d472376"
    client = TestClient(app)
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 204

def test_delete_invalid_chat():
    chat_id = "w2"
    client = TestClient(app)
    response = client.delete(f"/chats/{chat_id}")
    assert response.status_code == 404
    assert response.json() == {
            "detail": {
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": "w2",
            },
        }
    
def test_get_messages():
    chat_id = "660c7a6bc1324e4488cafabc59529c93"
    client = TestClient(app)
    response = client.get(f"/chats/{chat_id}/messages")
    assert response.status_code == 200
    assert response.json() == {
            "meta": {
                "count": 19,
            },
            "messages": [
                {
                    "id": "e8d32fbfdd0d493e8b9688eb9849f751",
                    "user_id": "reese",
                    "text": "But outside, it's living human tissue.  Flesh, skin, hair...blood.  Grown for the cyborgs.",
                    "created_at": "2023-04-12T20:26:37"
                },
                {
                    "id": "12d34362c49c455faa50d727081e3b2a",
                    "user_id": "sarah",
                    "text": "Look, Reese, I know you want to help, but...",
                    "created_at": "2023-04-12T20:26:44"
                },
                {
                    "id": "af78cdaafb05454bb4dd991c823d2e0b",
                    "user_id": "reese",
                    "text": "Pay attention.  The 600 series had rubber skin. We spotted them easy.  But these are new.  They look human.  Sweat, bad breath, everything.  Very hard to spot.  I had to wait 'til he moved on you before I could zero him.",
                    "created_at": "2023-04-12T20:29:15"
                },
                {
                    "id": "d297e59f96a740e7bd9a4a67fa65b972",
                    "user_id": "sarah",
                    "text": "Hey, I'm not stupid, y'know. They can't build anything like that yet.",
                    "created_at": "2023-04-12T20:33:32"
                },
                {
                    "id": "fbbe2127b07240c4891b2328a96d2238",
                    "user_id": "reese",
                    "text": "No.  Not yet.  Not for about forty years.",
                    "created_at": "2023-04-12T20:40:49"
                },
                {
                    "id": "dbf700308694454290c61597153cc4e6",
                    "user_id": "sarah",
                    "text": "So, it's from the future, is that right?",
                    "created_at": "2023-04-12T20:45:19"
                },
                {
                    "id": "9ff32ec2f0624f07952805e4fa579ff7",
                    "user_id": "reese",
                    "text": "One possible future.  Four your point of view.  I don't know the tech stuff.",
                    "created_at": "2023-04-12T20:46:45"
                },
                {
                    "id": "7e3ceed4fa0f4bf1972df743ad97481a",
                    "user_id": "sarah",
                    "text": "And you're from the future too?",
                    "created_at": "2023-04-12T20:48:53"
                },
                {
                    "id": "403b96920bb24e65a68b3c65505055ac",
                    "user_id": "reese",
                    "text": "Right.",
                    "created_at": "2023-04-12T20:54:37"
                },
                {
                    "id": "89356ed373f94ccca6c6a688562238ce",
                    "user_id": "sarah",
                    "text": "Just let me go.",
                    "created_at": "2023-04-12T20:56:49"
                },
                {
                    "id": "259cb82a0a704c83af4f0920a0416b74",
                    "user_id": "reese",
                    "text": "Listen.  Understand.  That Terminator is out there.  It can't be reasoned with, it can't be bargained with...it doesn't feel pity of remorse or fear... and it absolutely will not stop. Ever.  Until you are dead.",
                    "created_at": "2023-04-12T20:58:14"
                },
                {
                    "id": "6852c6bb5e794c17a7db6656488501bc",
                    "user_id": "reese",
                    "text": "There's so much...",
                    "created_at": "2023-04-12T20:59:10"
                },
                {
                    "id": "e96dad9e695744e2a6f2412e8426e865",
                    "user_id": "sarah",
                    "text": "Tell me.  Just start at the beginning.",
                    "created_at": "2023-04-12T21:01:41"
                },
                {
                    "id": "39d05912c9434c328c7ccf4e54e99627",
                    "user_id": "reese",
                    "text": "--everythingis gone.  Just gone.  There were survivors. Here.  There.  Nobody knew who started it.  It was the machines.",
                    "created_at": "2023-04-12T21:04:20"
                },
                {
                    "id": "03c317fa0c8c454b8aef21dcea07ab69",
                    "user_id": "sarah",
                    "text": "I don't understand...",
                    "created_at": "2023-04-12T21:10:22"
                },
                {
                    "id": "e4d484e5824c49f088d0719fe3a5671e",
                    "user_id": "reese",
                    "text": "Defense network computer. New. Powerful.  Hooked into everything. Trusted to run it all.  They say it got smart...a new order of intelli- gence.  Then it saw all people as a threat, not just the ones on the other side.  Decided out fate in a microsecond...extermination.",
                    "created_at": "2023-04-12T21:16:01"
                },
                {
                    "id": "f8776427558844ec904e83693bc87761",
                    "user_id": "reese",
                    "text": "Didn't see the war.  I was born after, in the ruins.  Grew up there.  Starving.  Hiding from the H-K's.",
                    "created_at": "2023-04-12T21:23:49"
                },
                {
                    "id": "4a8587f3568441f3a713916be8902364",
                    "user_id": "sarah",
                    "text": "The what?",
                    "created_at": "2023-04-12T21:25:47"
                },
                {
                    "id": "75a36b1177c448cdaf6c484a63139ef1",
                    "user_id": "reese",
                    "text": "Hunter Killers.  Patrol machines. Build in automated factories. Most of us were rounded up, put in camps...for orderly disposal.",
                    "created_at": "2023-04-12T21:30:12"
                }
            ],
        }
    

def test_get_invalid_messages():
    chat_id = "111"
    client = TestClient(app)
    response = client.get(f"/chats/{chat_id}/messages")
    assert response.status_code == 404
    assert response.json() == {
            "detail": {
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": "111",
            },
        }
    
def test_get_users_in_chat():
    chat_id = "6ad56d52b138432a9bba609533015cf3"
    client = TestClient(app)
    response = client.get(f"/chats/{chat_id}/users")
    assert response.status_code == 200
    assert response.json() == {
            "meta": {
                "count": 2,
            },
            "users": [
                {
                    "id": "doolittle",
                    "created_at": "2003-05-21T06:14:11"
                },
                {
                    "id": "talby",
                    "created_at": "2001-01-09T01:27:14"
                }
            ]
        }

def test_get_users_in_invalid_chat():
    chat_id = "55"
    client = TestClient(app)
    response = client.get(f"/chats/{chat_id}/users")
    assert response.status_code == 404
    assert response.json() == {
            "detail": {
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": "55",
            },
        }