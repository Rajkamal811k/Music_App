from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.user import User
from app.models.enums import UserRole
from app.core.security import hash_password

from app.core.config import settings


def create_admin():

    db = SessionLocal()

    try:

        existing_admin = db.scalar(
            select(User).where(
                User.role == UserRole.ADMIN
            )
        )

        if existing_admin:

            print("Admin account already exists.")
            return

        existing_user = db.scalar(
            select(User).where(
                (User.email == settings.ADMIN_EMAIL) |
                (User.username == settings.ADMIN_USERNAME)
            )
        )

        if existing_user:

            print("Username or email already belongs to another user.")
            return

        admin = User(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            password_hash=hash_password(
                settings.ADMIN_PASSWORD
            ),
            role=UserRole.ADMIN
        )

        db.add(admin)
        db.commit()

        print("Admin account created successfully.")

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


if __name__ == "__main__":
    create_admin()