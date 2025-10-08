from pydantic import BaseModel, ConfigDict

class FileLinkBase(BaseModel):
    message_id: int
    link: str

class FileLinkCreate(FileLinkBase):
    pass

class FileLinkRead(FileLinkBase):
    id: int
    model_config = ConfigDict(from_attributes=True)