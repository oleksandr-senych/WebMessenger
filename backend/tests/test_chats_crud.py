import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database.core import SessionLocal, engine, Base
from app.models import User


client = TestClient(app)

@pytest.mark.crud
def test_create_chat(create_user):
    user1 = create_user("user1", "user1@example.com")
    user2 = create_user("user2", "user2@example.com")

    response = client.post("api/chats/", json={
        "username1": user1.username,
        "username2": user2.username
    })
    assert response.status_code in (200, 201), f"Unexpected status {response.status_code}, response: {response.json()}"
    data = response.json()
    assert "id" in data
    assert data["user_id1"] == user1.id
    assert data["user_id2"] == user2.id

@pytest.mark.crud
def test_get_chats_for_user(db_session, create_user):
    user1 = create_user("user1", "user1@example.com")
    response = client.get(f"api/chats/{user1.username}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.crud
def test_delete_chat(test_db):
    #should be a better solution, than assigning constant id.
    chat_id = 1
    response = client.delete(f"api/chats/{chat_id}")
    assert response.status_code == 204



