from fastapi import FastAPI
from app.routes import users,chats,messages,filelinks

app = FastAPI(title="Webmessenger API")
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(chats.router, prefix="/api/chats", tags=["Chats"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(filelinks.router, prefix="/api/filelinks", tags=["Filelinks"])