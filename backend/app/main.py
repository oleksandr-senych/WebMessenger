from fastapi import FastAPI
from app.routes import users,chats

app = FastAPI(title="Webmessenger API")
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(chats.router, prefix="/api/chats", tags=["Chats"])