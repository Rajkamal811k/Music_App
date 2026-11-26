from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models.album import Album
from app.models.user import User
from app.models.enums import UserRole

from app.schemas.album import AlbumCreate, AlbumUpdate

from app.repositories import album_repository


def create_album(
    db: Session,
    user: User,
    data: AlbumCreate
):

    album = Album(
        **data.model_dump(),
        creator_id=user.id
    )

    return album_repository.create_album(
        db,
        album
    )


def get_album(
    db: Session,
    album_id: int
):

    album = album_repository.get_album_by_id(
        db,
        album_id
    )

    if not album:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Album not found"
        )

    return album


def get_all_albums(
    db: Session,
    skip: int = 0,
    limit: int = 10
):

    return album_repository.get_all_albums(
        db,
        skip,
        limit
    )


def get_my_albums(
    db: Session,
    user: User
):

    return album_repository.get_albums_by_creator(
        db,
        user.id
    )


def update_album(
    db: Session,
    user: User,
    album_id: int,
    data: AlbumUpdate
):

    album = get_album(db, album_id)

    # Ownership validation

    if album.creator_id != user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot update another creator's album"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():

        setattr(album, field, value)

    return album_repository.update_album(
        db,
        album
    )


def delete_album(
    db: Session,
    user: User,
    album_id: int
):

    album = get_album(db, album_id)

    # Admin can delete any album.
    # Creator can delete only their own album.

    is_admin = user.role == UserRole.ADMIN

    is_owner = album.creator_id == user.id

    if not is_admin and not is_owner:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot delete this album"
        )

    album_repository.delete_album(
        db,
        album
    )

    return {
        "message": "Album deleted successfully"
    }