from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.enums import UserRole

from app.models.creator_profile import CreatorProfile

from app.schemas.creator import (
    CreatorProfileCreate,
    CreatorProfileUpdate
)

from app.repositories import creator_repository


def create_profile(
    db: Session,
    user: User,
    data: CreatorProfileCreate
):

    if user.role != UserRole.CREATOR:

        raise HTTPException(
            status_code=403,
            detail="Only creators can create creator profiles"
        )

    existing = creator_repository.get_by_user_id(
        db,
        user.id
    )

    if existing:

        raise HTTPException(
            status_code=409,
            detail="Creator profile already exists"
        )

    profile = CreatorProfile(
        user_id=user.id,
        **data.model_dump()
    )

    return creator_repository.create(
        db,
        profile
    )


def get_profile(
    db: Session,
    user: User
):

    profile = creator_repository.get_by_user_id(
        db,
        user.id
    )

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Creator profile not found"
        )

    return profile


def update_profile(
    db: Session,
    user: User,
    data: CreatorProfileUpdate
):

    profile = get_profile(db, user)

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(profile, field, value)

    db.commit()

    db.refresh(profile)

    return profile