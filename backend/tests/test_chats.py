import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database.core import SessionLocal, engine, Base
from app.models import User


client = TestClient(app)

@pytest.mark.crud
def test_create_chat(create_user,login_user):
    user1 = create_user("user1")
    user2 = create_user("user2")
    
    header=login_user("user1")

    response = client.post("api/chats/", json={
        "other_username": "user2",
    },headers=header)
    assert response.status_code in (200, 201), f"Unexpected status {response.status_code}, response: {response.json()}"
    data = response.json()
    assert "id" in data
    print(data)
    assert data["username1"] == "user1"
    assert data["username2"] == "user2"

@pytest.mark.crud
def test_get_chats_for_user( create_user, login_user):
    user1 = create_user("user1")
    header=login_user("user1")
    response = client.get(f"api/chats/",headers=header)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.crud
def test_delete_chat(create_user,login_user):
    header = login_user("user1")
    chat_id = 1
    response = client.delete(f"api/chats/{chat_id}",headers=header)
    assert response.status_code == 204



