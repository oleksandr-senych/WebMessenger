import pytest
from app.database.core import SessionLocal, engine, Base
from app.models import User
from app.database.init_db import init_db






# new_user = User(username="testuser", email="test@example.com", hashed_password="hashed_test_pass")
# db.add(new_user)
# db.commit()
# db.refresh(new_user)  # Refresh to get the generated ID


@pytest.mark.db
def test_get_users():

    # Make sure tables exist
    init_db()

    print("Connecting to database...")


    # Create a database session
    db = SessionLocal()

    try:
        users = db.query(User).all()
        print(f"Database connection successful — found {len(users)} users.")
        for user in users:
            print(f"User: {user.username}")
    finally:
        db.close()