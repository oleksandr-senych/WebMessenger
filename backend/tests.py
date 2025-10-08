from app.database import SessionLocal, engine, Base
from app.models import User
from app.init_db import init_db

# Make sure tables exist
print("Connecting to database...")
Base.metadata.create_all(bind=engine)

# Create a database session
db = SessionLocal()

# new_user = User(username="testuser", email="test@example.com", hashed_password="hashed_test_pass")
# db.add(new_user)
# db.commit()
# db.refresh(new_user)  # Refresh to get the generated ID

print("Connecting to database...")
try:
    users = db.query(User).all()
    print(f"Database connection successful — found {len(users)} users.")
    for user in users:
        print(f"User: {user.username}")
finally:
    db.close()