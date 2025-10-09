from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.database.core import get_db
from app.models import User, Chat
from app.schemas.user import UserCreate, UserRead
from app.schemas.chat import ChatRead,ChatCreate
from app.security import get_current_user


router = APIRouter()


#Creates chat when both usernames are known
@router.post("/", response_model=ChatRead)
def create_chat(chat_create: ChatCreate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user),
                status_code=status.HTTP_201_CREATED
):

    other_user = db.query(User).filter(User.username == chat_create.username).first()

    if not other_user:
        raise HTTPException(status_code=404, detail="User not found")

    if other_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot create chat with yourself")

    existing_chat = db.query(Chat).filter(
        ((Chat.user_id1 == current_user.id) & (Chat.user_id2 == other_user.id)) |
        ((Chat.user_id1 == other_user.id) & (Chat.user_id2 == current_user.id))
    ).first()

    if existing_chat:
        return existing_chat

    db_chat = Chat(user1=current_user, user2=other_user) 
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

# Get all chats for current user
@router.get("/", response_model=list[ChatRead])
def get_my_chats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    chats = (
        db.query(Chat)
        .options(selectinload(Chat.user1), selectinload(Chat.user2))
        .filter((Chat.user_id1 == current_user.id) | (Chat.user_id2 == current_user.id))
        .all()
    )
    return chats

# Delete a chat by ID (only if user is a participant)
@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    if current_user.id not in [chat.user_id1, chat.user_id2]:
        raise HTTPException(status_code=403, detail="You can only delete your own chats")

    db.delete(chat)
    db.commit()
    return