from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.core import get_db
from app.models import User, Chat
from app.schemas.user import UserCreate, UserRead
from app.schemas.chat import ChatRead,ChatCreate


router = APIRouter()


#Creates chat when both usernames are known
@router.post("/", response_model=ChatRead)
def create_chat(chat_create: ChatCreate, db: Session = Depends(get_db), status_code=status.HTTP_201_CREATED):

    user1 = db.query(User).filter(User.username == chat_create.username1).first()
    user2 = db.query(User).filter(User.username == chat_create.username2).first()

    if not user1 or not user2:
        raise HTTPException(status_code=404, detail="One or both usernames not found")

    if user1.id == user2.id:
        raise HTTPException(status_code=400, detail="Cannot create chat with same user")

    existing_chat = db.query(Chat).filter(
        ((Chat.user_id1 == user1.id) & (Chat.user_id2 == user2.id)) |
        ((Chat.user_id1 == user2.id) & (Chat.user_id2 == user1.id))
    ).first()

    if existing_chat:
        return existing_chat

    db_chat = Chat(user1=user1, user2=user2) 
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

# Retreives all chats of user
@router.get("/{username}", response_model=list[ChatRead])
def get_all_chats(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    chats = db.query(Chat).filter(
        (Chat.user_id1 == user.id) | (Chat.user_id2 == user.id)
    ).all()

    return chats

@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    db.delete(chat)
    db.commit()