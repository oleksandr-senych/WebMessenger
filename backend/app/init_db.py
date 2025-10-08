from .database import Base, engine
from .models import User, Message, Chat, FileLink

# Create Tables
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()