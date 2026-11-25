from sqlalchemy import Index, text
from datetime import datetime, timezone

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    Enum,
    Boolean
)

from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base
from app.models.enums import UserRole


class User(Base):
    __table_args__ = (
    Index(
        "uq_users_single_admin",
        "role",
        unique=True,
        postgresql_where=text("role = 'ADMIN'")
    ),
)

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False),
        default=UserRole.USER,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    full_name: Mapped[str | None] = mapped_column(
    String(100),
    nullable=True
    )

    avatar_url: Mapped[str | None] = mapped_column(
    String(500),
    nullable=True
    )