from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.core import Base
from .user import User

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id1 = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_id2 = Column(Integer, ForeignKey("users.id"), nullable=False)

    user1 = relationship("User", foreign_keys=[user_id1])
    user2 = relationship("User", foreign_keys=[user_id2])

    @property
    def username1(self):
        return self.user1.username if self.user1 else None

    @property
    def username2(self):
        return self.user2.username if self.user2 else None

    messages = relationship("Message", back_populates="chat")