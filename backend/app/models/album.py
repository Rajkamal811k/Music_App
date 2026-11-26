from datetime import datetime, timezone, date

from sqlalchemy import (
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class Album(Base):

    __tablename__ = "albums"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True
    )

    artist: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    cover_image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    release_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )