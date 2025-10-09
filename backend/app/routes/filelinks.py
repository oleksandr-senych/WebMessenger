from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.core import get_db
from app.models import Message
from app.models.filelink import FileLink
from app.schemas.filelink import FileLinkRead, FileLinkCreate


router = APIRouter()


#Add filelink to a message
@router.post("/", response_model=FileLinkRead, status_code=status.HTTP_201_CREATED)
def create_filelink(filelink_create: FileLinkCreate, db: Session = Depends(get_db)):
    message = db.get(Message, filelink_create.message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    filelink = FileLink(message_id=filelink_create.message_id, link=filelink_create.link)
    db.add(filelink)
    db.commit()
    db.refresh(filelink)

    return filelink

# Delete filelink
@router.delete("/{filelink_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(filelink_id: int, db: Session = Depends(get_db)):
    filelink = db.get(FileLink, filelink_id)
    if not filelink:
        raise HTTPException(status_code=404, detail="Filelink not found")

    db.delete(filelink)
    db.commit()
    return