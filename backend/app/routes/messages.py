from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,selectinload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.database.core import get_db
from app.models import Message, Chat, FileLink, User
from app.schemas.message import MessageCreate,MessageRead, MessageUpdate
from app.security import get_current_user

router = APIRouter()

# Adds messages with filelinks to db
@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
def create_messagecreate_message(
    message_create: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Ensure chat exists
    chat = db.get(Chat, message_create.chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if current_user.id not in [chat.user_id1, chat.user_id2]:
        raise HTTPException(status_code=403, detail="You cannot send messages in this chat")

    # Create message
    new_message = Message(
        chat_id=message_create.chat_id,
        user = current_user,
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
def get_all_messages(
    chat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chat = (
        db.query(Chat)
        .options(
            selectinload(Chat.messages).selectinload(Message.filelinks)
        )
        .get(chat_id)
    )

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    if current_user.id not in [chat.user_id1, chat.user_id2]:
        raise HTTPException(status_code=403, detail="Access denied")

    return sorted(chat.messages, key=lambda m: m.created_at)

# Updates message text
@router.put("/{message_id}", response_model=MessageRead, status_code=status.HTTP_200_OK)
def update_message(
    message_id: int,
    new_text: MessageUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    message = db.get(Message, message_id)

    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if message.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only edit your own messages")

    message.text= new_text.text
    db.commit()
    db.refresh(message)
    return message


# Delete message
@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    message = db.get(Message, message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    if message.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own messages")

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
