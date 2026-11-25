from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.core.dependencies import require_role

from app.models.user import User
from app.models.enums import UserRole

from app.schemas.creator import (
    CreatorProfileCreate,
    CreatorProfileUpdate,
    CreatorProfileResponse
)

from app.services import creator_service


router = APIRouter(
    prefix="/creators",
    tags=["Creators"]
)


creator_access = require_role(UserRole.CREATOR)


@router.post(
    "/profile",
    response_model=CreatorProfileResponse
)
def create_creator_profile(
    data: CreatorProfileCreate,
    current_user: User = Depends(creator_access),
    db: Session = Depends(get_db)
):

    return creator_service.create_profile(
        db,
        current_user,
        data
    )


@router.get(
    "/profile",
    response_model=CreatorProfileResponse
)
def get_creator_profile(
    current_user: User = Depends(creator_access),
    db: Session = Depends(get_db)
):

    return creator_service.get_profile(
        db,
        current_user
    )


@router.patch(
    "/profile",
    response_model=CreatorProfileResponse
)
def update_creator_profile(
    data: CreatorProfileUpdate,
    current_user: User = Depends(creator_access),
    db: Session = Depends(get_db)
):

    return creator_service.update_profile(
        db,
        current_user,
        data
    )