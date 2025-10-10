from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from app.schemas.filelink import FileLinkCreate, FileLinkRead

class MessageBase(BaseModel):
    chat_id: int
    user_id: int
    text: str | None = None

class MessageCreate(BaseModel):
    chat_id: int
    text: Optional[str] = None
    filelinks: Optional[List[FileLinkCreate]] = []

class MessageUpdate(BaseModel):
    text: str


class MessageRead(MessageBase):
    id: int
    created_at: datetime
    username: Optional[str] = None
    filelinks: List[FileLinkRead] = []
    model_config = ConfigDict(from_attributes=True)