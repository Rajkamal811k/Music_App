from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Song(Base):

    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True
    )

    artist: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True
    )

    album: Mapped[str] = mapped_column(
        String(200),
        nullable=True,
        default=""
    )

    genre: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        default=""
    )

    duration: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    file_path: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    cover_image_path: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    uploaded_by: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
