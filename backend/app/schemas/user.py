from pydantic import BaseModel, Field, ConfigDict


class UserProfileUpdate(BaseModel):

    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    avatar_url: str | None = Field(
        default=None,
        max_length=500
    )


class UserProfileResponse(BaseModel):

    id: int
    username: str
    email: str
    full_name: str | None
    avatar_url: str | None
    role: str

    model_config = ConfigDict(
        from_attributes=True
    )