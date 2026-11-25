from sqlalchemy import (
    Integer,
    String,
    Text,
    ForeignKey
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class CreatorProfile(Base):

    __tablename__ = "creator_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    artist_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    website: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )