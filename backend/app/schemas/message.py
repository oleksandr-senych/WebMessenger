from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MessageBase(BaseModel):
    chat_id: int
    user_id: int
    text: str | None = None

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)