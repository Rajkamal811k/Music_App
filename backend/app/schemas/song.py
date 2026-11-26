from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SongCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    lyrics: str | None = None
    genre: str = Field(min_length=2, max_length=100)
    duration_seconds: int = Field(gt=0)

    # Optional: standalone songs are allowed.
    album_id: int | None = None


class SongUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=150)
    lyrics: str | None = None
    genre: str | None = Field(default=None, min_length=2, max_length=100)
    duration_seconds: int | None = Field(default=None, gt=0)
    album_id: int | None = None


class SongResponse(BaseModel):
    id: int
    title: str
    lyrics: str | None
    genre: str
    duration_seconds: int
    album_id: int | None
    creator_id: int
    audio_storage_path: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)