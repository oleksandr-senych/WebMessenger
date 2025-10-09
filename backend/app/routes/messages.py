from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,selectinload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.database.core import get_db
from app.models import Message, Chat, FileLink
from app.schemas.message import MessageCreate,MessageRead, MessageUpdate

router = APIRouter()

# Adds messages with filelinks to db
@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
def create_message(message_create: MessageCreate, db: Session = Depends(get_db)):

    # Ensure chat exists
    chat = db.get(Chat, message_create.chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Create message
    new_message = Message(
        chat_id=message_create.chat_id,
        user_id=message_create.user_id,
        text=message_create.text
    )

    # Add file links
    if message_create.filelinks:
        for fl in message_create.filelinks:
            new_message.filelinks.append(FileLink(link=fl.link))

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message

# Retreives all messages from a chat
@router.get("/{chat_id}", response_model=list[MessageRead])
def get_all_messages(chat_id: int, db: Session = Depends(get_db)):
    chat = (
        db.query(Chat)
        .options(
            selectinload(Chat.messages).selectinload(Message.filelinks)
        )
        .get(chat_id)
    )

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return sorted(chat.messages, key=lambda m: m.created_at)

# Updates message text
@router.put("/{message_id}", response_model=MessageRead)
def update_message(message_id: int, new_text: MessageUpdate, db: Session = Depends(get_db)):
    message = db.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    message.text= new_text
    db.commit()
    db.refresh(message)
    return message


# Delete message
@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(message_id: int, db: Session = Depends(get_db)):
    message = db.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    try:
        db.delete(message)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete message due to integrity constraints: {str(e.orig)}"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while deleting the message: {str(e)}"
        )
    return
