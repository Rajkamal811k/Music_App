from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.core.dependencies import (
    get_current_user,
    require_role,
)

from app.models.user import User
from app.models.enums import UserRole

from app.schemas.song import (
    SongCreate,
    SongUpdate,
    SongResponse,
)

from app.services import song_service


router = APIRouter(
    prefix="/songs",
    tags=["Songs"],
)

creator_access = require_role(UserRole.CREATOR)


@router.post(
    "",
    response_model=SongResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_song(
    data: SongCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(creator_access),
):
    return song_service.create_song(
        db,
        data,
        current_user,
    )


@router.get(
    "",
    response_model=list[SongResponse],
)
def get_songs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return song_service.get_songs(
        db,
        skip,
        limit,
    )


# Keep this route before /{song_id}.
@router.get(
    "/my-songs",
    response_model=list[SongResponse],
)
def get_my_songs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(creator_access),
):
    return song_service.get_my_songs(
        db,
        current_user,
        skip,
        limit,
    )


@router.get(
    "/{song_id}",
    response_model=SongResponse,
)
def get_song(
    song_id: int,
    db: Session = Depends(get_db),
):
    return song_service.get_song(db, song_id)


@router.patch(
    "/{song_id}",
    response_model=SongResponse,
)
def update_song(
    song_id: int,
    data: SongUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(creator_access),
):
    return song_service.update_song(
        db,
        song_id,
        data,
        current_user,
    )


@router.delete("/{song_id}")
def delete_song(
    song_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return song_service.delete_song(
        db,
        song_id,
        current_user,
    )