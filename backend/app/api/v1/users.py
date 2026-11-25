from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.core.dependencies import get_current_user

from app.models.user import User

from app.schemas.user import (
    UserProfileUpdate,
    UserProfileResponse
)

from app.services import user_service


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/profile",
    response_model=UserProfileResponse
)
def get_profile(
    current_user: User = Depends(get_current_user)
):

    return current_user


@router.patch(
    "/profile",
    response_model=UserProfileResponse
)
def update_profile(
    data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return user_service.update_profile(
        db,
        current_user,
        data
    )