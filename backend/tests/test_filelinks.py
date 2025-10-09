import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, Chat, Message, FileLink

client = TestClient(app)


@pytest.mark.crud
def test_add_filelink(db_session, create_user, create_chat, create_message):
    chat = create_chat("filelink_user1", "filelink_user2")
    message = create_message(chat.id, chat.user_id1, "Test message")

    payload = {"link": "https://example.com/testfile.png", "message_id": message.id}

    response = client.post("/api/filelinks/", json=payload)
    assert response.status_code in (200, 201), f"Unexpected status {response.status_code}, {response.json()}"

    data = response.json()
    assert "id" in data
    assert data["link"] == payload["link"]
    assert data["message_id"] == message.id


@pytest.mark.crud
def test_delete_filelink(db_session, create_user, create_chat, create_message, create_filelink):
    chat = create_chat("filelink_user3", "filelink_user4")
    message = create_message(chat.id, chat.user_id1, "Message with filelink")
    filelink = create_filelink("https://example.com/deletefile.png", message.id)

    response = client.delete(f"/api/filelinks/{filelink.id}")
    assert response.status_code == 204

    # Ensure it's deleted
    get_resp = client.get(f"/api/filelinks/{filelink.id}")
    assert get_resp.status_code == 405