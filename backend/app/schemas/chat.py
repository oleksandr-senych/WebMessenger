from pydantic import BaseModel, ConfigDict

class ChatBase(BaseModel):
    user_id1: int
    user_id2: int


#first username is known by jwt authentication
class ChatCreate(BaseModel):
    other_username: str

class ChatRead(ChatBase):
    id: int
    username1: str
    username2: str
    model_config = ConfigDict(from_attributes=True)