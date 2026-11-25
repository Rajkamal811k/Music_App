from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.creator_profile import CreatorProfile


def get_by_user_id(
    db: Session,
    user_id: int
):

    statement = select(CreatorProfile).where(
        CreatorProfile.user_id == user_id
    )

    return db.scalar(statement)


def create(
    db: Session,
    profile: CreatorProfile
):

    db.add(profile)

    db.commit()

    db.refresh(profile)

    return profile