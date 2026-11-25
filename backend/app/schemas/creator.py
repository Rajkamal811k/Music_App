from pydantic import BaseModel, Field, ConfigDict


class CreatorProfileCreate(BaseModel):

    artist_name: str = Field(
        min_length=2,
        max_length=100
    )

    bio: str | None = None

    website: str | None = Field(
        default=None,
        max_length=255
    )


class CreatorProfileUpdate(BaseModel):

    artist_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    bio: str | None = None

    website: str | None = Field(
        default=None,
        max_length=255
    )


class CreatorProfileResponse(BaseModel):

    id: int
    user_id: int
    artist_name: str
    bio: str | None
    website: str | None

    model_config = ConfigDict(
        from_attributes=True
    )