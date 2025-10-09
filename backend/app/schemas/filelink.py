from typing import Optional
from pydantic import BaseModel, ConfigDict

class FileLinkBase(BaseModel):
    message_id: int
    link: str

class FileLinkCreate(BaseModel):
    link: str
    message_id: Optional[int] = None


class FileLinkRead(FileLinkBase):
    id: int
    model_config = ConfigDict(from_attributes=True)