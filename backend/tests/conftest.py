import os
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.core import Base, get_db
from app.models import User, Chat, Message, FileLink
from app.main import app



TEST_DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_TEST_NAME')}"
)

test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Creates all tables at the start of tests. Deletes all tables after the tests.
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

# Creates db session
@pytest.fixture
def db_session(test_db):
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
# --- FASTAPI OVERRIDE ---
def override_get_db():
    """Override FastAPI's DB dependency for testing."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
                
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def create_user(db_session):
    def _create(username : str, password : str = "secret123"):
        response = client.post(
            "/api/auth/register",
            json={
                "username": username,
                "email": f"{username}@example.com",
                "password": password
            }
        )
        assert response.status_code in (200, 201), f"Failed to create user: {response.text}"
        return username
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
        user1 = create_user(username1)
        user2 = create_user(username2)

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