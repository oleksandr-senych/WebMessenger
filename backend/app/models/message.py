from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database.core import Base
from .chat import Chat
from .user import User

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), index=True, server_default=func.now())

    chat = relationship("Chat", back_populates="messages")
    user = relationship("User", back_populates="messages")

    @property
    def username(self):
        return self.user.username if self.user else None
    
    filelinks = relationship("FileLink", back_populates="message", cascade="all, delete-orphan")