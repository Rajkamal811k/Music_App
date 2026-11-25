from fastapi import FastAPI

from app.core.config import settings

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.creators import router as creators_router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)


app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    users_router,
    prefix="/api/v1"
)

app.include_router(
    creators_router,
    prefix="/api/v1"
)


@app.get("/")
def home():

    return {
        "message": "Music Streaming API",
        "status": "running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }