from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.core.dependencies import (
    get_current_user,
    require_role
)

from app.models.user import User
from app.models.enums import UserRole

from app.schemas.album import (
    AlbumCreate,
    AlbumUpdate,
    AlbumResponse
)

from app.services import album_service


router = APIRouter(
    prefix="/albums",
    tags=["Albums"]
)


creator_access = require_role(
    UserRole.CREATOR
)


# Create Album

@router.post(
    "",
    response_model=AlbumResponse,
    status_code=status.HTTP_201_CREATED
)
def create_album(
    data: AlbumCreate,
    current_user: User = Depends(creator_access),
    db: Session = Depends(get_db)
):

    return album_service.create_album(
        db,
        current_user,
        data
    )


# Get All Albums

@router.get(
    "",
    response_model=list[AlbumResponse]
)
def get_all_albums(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):

    return album_service.get_all_albums(
        db,
        skip,
        limit
    )


# Get My Albums

@router.get(
    "/my-albums",
    response_model=list[AlbumResponse]
)
def get_my_albums(
    current_user: User = Depends(creator_access),
    db: Session = Depends(get_db)
):

    return album_service.get_my_albums(
        db,
        current_user
    )


# Get Album By ID

@router.get(
    "/{album_id}",
    response_model=AlbumResponse
)
def get_album(
    album_id: int,
    db: Session = Depends(get_db)
):

    return album_service.get_album(
        db,
        album_id
    )


# Update Album

@router.patch(
    "/{album_id}",
    response_model=AlbumResponse
)
def update_album(
    album_id: int,
    data: AlbumUpdate,
    current_user: User = Depends(creator_access),
    db: Session = Depends(get_db)
):

    return album_service.update_album(
        db,
        current_user,
        album_id,
        data
    )


# Delete Album

@router.delete(
    "/{album_id}"
)
def delete_album(
    album_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return album_service.delete_album(
        db,
        current_user,
        album_id
    )