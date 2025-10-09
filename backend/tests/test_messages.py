import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Message

client = TestClient(app)


@pytest.mark.crud
def test_create_message(db_session, create_user, create_chat):
    chat = create_chat("user_msg1", "user_msg2")

    payload = {
        "chat_id": chat.id,
        "user_id": chat.user_id1,
        "text": "Hello, this is a test message!",
        "filelinks": [{"link": "https://example.com/file1.png"}]
    }

    response = client.post("api/messages/", json=payload)
    assert response.status_code in (200, 201), f"Unexpected status {response.status_code}, response: {response.json()}"
    data = response.json()
    assert data["chat_id"] == chat.id
    assert data["user_id"] == chat.user_id1
    assert data["text"] == payload["text"]
    assert "filelinks" in data
    assert len(data["filelinks"]) == 1


@pytest.mark.crud
def test_get_all_messages(create_user, create_chat):
    chat = create_chat("user_msg3", "user_msg4")

    client.post("api/messages/", json={
        "chat_id": chat.id,
        "user_id": chat.user_id1,
        "text": "Message 1"
    })
    client.post("api/messages/", json={
        "chat_id": chat.id,
        "user_id": chat.user_id2,
        "text": "Message 2"
    })

    response = client.get(f"api/messages/{chat.id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2
    assert data[0]["text"] == "Message 1"


@pytest.mark.crud
def test_update_message(create_user, create_chat):
    chat = create_chat("user_msg5", "user_msg6")

    response = client.post("api/messages/", json={
        "chat_id": chat.id,
        "user_id": chat.user_id1,
        "text": "Old text"
    })
    message_id = response.json()["id"]

    new_text = "Updated text"
    update_resp = client.put(f"api/messages/{message_id}", json={"text": new_text})
    assert update_resp.status_code in (200,201), f"Unexpected status {response.status_code}, response: {response.json()}"
    updated_message = update_resp.json()
    assert updated_message["text"] == new_text


@pytest.mark.crud
def test_delete_message(create_user, create_chat):
    chat = create_chat("user_msg7", "user_msg8")

    response = client.post("api/messages/", json={
        "chat_id": chat.id,
        "user_id": chat.user_id1,
        "text": "Delete me"
    })
    message_id = response.json()["id"]

    del_resp = client.delete(f"api/messages/{message_id}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"api/messages/{chat.id}")
    messages = get_resp.json()
    assert all(msg["id"] != message_id for msg in messages)


