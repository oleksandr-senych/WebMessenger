from fastapi import FastAPI
from app.routes import users

app = FastAPI(title="Webmessenger API")
app.include_router(users.router, prefix="/api/users", tags=["Users"])