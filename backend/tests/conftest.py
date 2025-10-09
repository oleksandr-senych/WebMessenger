from fastapi.testclient import TestClient
import pytest
from app.database.core import SessionLocal, Base, engine
from app.models import User, Chat, Message, FileLink
from app.main import app

client = TestClient(app)

# Creates all tables at the start of tests. Deletes all tables after the tests.
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Creates db session
@pytest.fixture
def db_session(test_db):
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def create_user(db_session):
    def _create(username : str, email : str, password : str = "secret123"):
        response = client.post(
            "/api/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )
        assert response.status_code in (200, 201), f"Failed to create user: {response.text}"
        return username, email
    return _create

@pytest.fixture
def login_user(db_session):
    def _login(username : str, password : str = "secret123"):
        response = client.post(
            "/api/auth/login",
            data={
                "username": username,
                "password": password
            }
        )
        # if login successful, return header
        if response.status_code == 200:
            token = response.json()["access_token"]
            return {"Authorization": f"Bearer {token}"}
        else :
            return response
    return _login

@pytest.fixture
def create_chat(db_session, create_user):
    def _create(username1, username2):
        user1 = create_user(username1, f"{username1}@example.com")
        user2 = create_user(username2, f"{username2}@example.com")

        chat = Chat(user_id1=user1.id, user_id2=user2.id)
        try:
            #if chat doesnt exist, add chat
            db_session.add(chat)
            db_session.commit()
            db_session.refresh(chat)
        finally:
            return chat
    return _create

@pytest.fixture
def create_message(db_session):
    def _create(chat_id, user_id, text):
        msg = Message(chat_id=chat_id, user_id=user_id, text=text)
        db_session.add(msg)
        db_session.commit()
        db_session.refresh(msg)
        return msg
    return _create


@pytest.fixture
def create_filelink(db_session):
    def _create(link, message_id):
        fl = FileLink(link=link, message_id=message_id)
        db_session.add(fl)
        db_session.commit()
        db_session.refresh(fl)
        return fl
    return _create