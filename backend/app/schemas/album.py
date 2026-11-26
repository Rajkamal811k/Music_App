from datetime import date, datetime

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


class AlbumCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=150
    )

    artist: str = Field(
        min_length=2,
        max_length=150
    )

    description: str | None = None

    cover_image_url: str | None = Field(
        default=None,
        max_length=500
    )

    release_date: date | None = None


class AlbumUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    artist: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    description: str | None = None

    cover_image_url: str | None = Field(
        default=None,
        max_length=500
    )

    release_date: date | None = None


class AlbumResponse(BaseModel):

    id: int

    name: str

    artist: str

    description: str | None

    cover_image_url: str | None

    release_date: date | None

    creator_id: int

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )