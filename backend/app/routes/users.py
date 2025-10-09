from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.core import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.security import get_current_user

router = APIRouter()

# Create user
# @router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     existing = db.query(User).filter(User.email == user.email).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     new_user = User(
#         username=user.username,
#         email=user.email,
#         hashed_password="hashing_not_implemented"
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# # Read all users
# @router.get("/", response_model=list[UserRead])
# def get_users(db: Session = Depends(get_db)):
#     return db.query(User).all()

# Return authenticated user
@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user

# @router.get("/{username}", response_model=UserRead)
# def get_user(username: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user





# Delete authenticated user
@router.delete("/me", status_code=204)
def delete_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return

# @router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(username: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     db.delete(user)
#     db.commit()
#     return
