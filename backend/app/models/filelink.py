from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.core import Base
from .message import Message

class FileLink(Base):
    __tablename__ = "filelinks"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    link = Column(String, nullable=False)

    message = relationship("Message", back_populates="filelinks")