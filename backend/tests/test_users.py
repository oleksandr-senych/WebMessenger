import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.core import SessionLocal, engine, Base
from app.models import User






client = TestClient(app)




@pytest.mark.auth
def test_register_user(test_db):
    test_username = "apitestuser"
    test_email = "apitest@example.com"
    test_password = "secret123"
    response = client.post(
        "api/auth/register",
        json={
            "username": test_username,
            "email": test_email,
            "password": test_password
        }
    )

    assert response.status_code in (200, 201), f"Unexpected status {response.status_code}, response: {response.json()}"
    data = response.json()
    assert data["username"] == test_username
    assert data["email"] == test_email

@pytest.mark.auth
def test_user_login(test_db):

    username = "testloginuser"
    email = "testlogin@example.com"
    password = "secret123"

    # Register user
    register_response = client.post(
        "/api/auth/register",
        json={"username": username, "email": email, "password": password}
    )

    assert register_response.status_code in (200, 201), \
        f"Register failed: {register_response.json()}"

    # Login attempt
    login_response = client.post(
        "/api/auth/login",
        data={"username": username, "password": password}
    )

    assert login_response.status_code == 200, \
        f"Login failed: {login_response.json()}"

    login_data = login_response.json()
    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"

    # attempt login with wrong password
    bad_login_response = client.post(
        "/api/auth/login",
        data={"username": username, "password": "wrongpassword"}
    )

    assert bad_login_response.status_code == 401
    assert bad_login_response.json()["detail"] == "Invalid username or password"



@pytest.mark.crud
def test_delete_user(create_user,login_user,test_db):
    username= create_user("apitestuser_delete")

    header = login_user(username)

    # Delete user
    delete_response = client.delete(f"/api/users/me", headers=header)
    assert delete_response.status_code == 204, f"Failed to delete user: {delete_response.text}"
    assert delete_response.content == b"", "DELETE response should have empty body"

    # try to login again
    get_response = login_user(username)
    assert get_response.status_code == 401, f"User still exists after deletion: {get_response.text}"