import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.core import SessionLocal, engine, Base
from app.models import User
from app.database.init_db import init_db





client = TestClient(app)

def cleanup_user(username: str):
    db = SessionLocal()
    try:
        db.query(User).filter(User.username == username).delete()
        db.commit()
    finally:
        db.close()


@pytest.mark.crud
def test_create_user():
    test_username = "apitestuser"
    test_email = "apitest@example.com"
    cleanup_user(test_username)
    response = client.post(
        "api/users/",
        json={
            "username": test_username,
            "email": test_email,
            "password": "secret123"
        }
    )

    if response.status_code in (200, 201):
        data = response.json()
        assert data["username"] == "apitestuser"
        assert "id" in data
    else:
        assert False, f"Unexpected status {response.status_code}, response: {response.json()}"


@pytest.mark.crud
def test_read_users():
    response = client.get("api/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)


@pytest.mark.crud
def test_get_user_by_username():
    test_username = "apitestuser_find"
    test_email = "apitest_find@example.com"

    cleanup_user(test_username)

    # Create user first
    response = client.post(
        "/api/users/",
        json={
            "username": test_username,
            "email": test_email,
            "password": "secret123"
        }
    )
    assert response.status_code in (200, 201), f"Create failed: {response.json()}"

    # Now test Get by username
    response = client.get(f"/api/users/{test_username}")
    assert response.status_code == 200, f"Unexpected status: {response.status_code}, {response.json()}"
    data = response.json()

    assert data["username"] == test_username, f"Expected username {test_username}, got {data['username']}"
    assert data["email"] == test_email, f"Expected email {test_email}, got {data['email']}"
    assert "id" in data

@pytest.mark.crud
def test_delete_user():
    test_username = "apitestuser_delete"
    test_email = "apitest_delete@example.com"

    
    cleanup_user(test_username)

    # Create user
    response = client.post(
        "/api/users/",
        json={
            "username": test_username,
            "email": test_email,
            "password": "secret123"
        }
    )
    assert response.status_code in (200, 201), f"Failed to create user: {response.text}"

    # Delete user
    delete_response = client.delete(f"/api/users/{test_username}")
    assert delete_response.status_code == 204, f"Failed to delete user: {delete_response.text}"
    assert delete_response.content == b"", "DELETE response should have empty body"


    get_response = client.get(f"/api/users/{test_username}")
    assert get_response.status_code == 404, f"User still exists after deletion: {get_response.text}"