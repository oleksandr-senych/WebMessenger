from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users,chats,messages,filelinks,auth
from app.database.init_db import init_db
from app.models import __all__
from app.database.core import Base


#Create tables if they don't exist
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    init_db()
    yield
    # Shutdown 
    print("Shutting down...")

# Allow frontend (e.g. Vite on localhost:5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]






app = FastAPI(title="Webmessenger API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],  # allow Authorization, Content-Type, etc.
)


app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(chats.router, prefix="/api/chats", tags=["Chats"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(filelinks.router, prefix="/api/filelinks", tags=["Filelinks"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])