import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings

from app.database.connection import Base, engine

import app.models

from app.api.v1.auth import router as auth_router
from app.api.v1.songs import router as songs_router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


# Create uploads directories
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(os.path.join(UPLOAD_DIR, "songs"), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_DIR, "covers"), exist_ok=True)

# Mount static files for uploads
app.mount(
    "/uploads",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "uploads")),
    name="uploads"
)


app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    songs_router,
    prefix="/api/v1"
)


@app.get("/")
def home():

    return {
        "message": "Music Streaming API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }
