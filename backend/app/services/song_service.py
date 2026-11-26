from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.song import Song
from app.models.user import User
from app.models.enums import UserRole

from app.schemas.song import SongCreate, SongUpdate

from app.repositories import song_repository
from app.repositories import album_repository


def create_song(
    db: Session,
    data: SongCreate,
    current_user: User,
):
    # Validate album ownership if an album was selected.
    if data.album_id is not None:
        album = album_repository.get_album_by_id(
            db,
            data.album_id,
        )

        if not album:
            raise HTTPException(
                status_code=404,
                detail="Album not found",
            )

        if album.creator_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only add songs to your own albums",
            )

    song = Song(
        title=data.title,
        lyrics=data.lyrics,
        genre=data.genre,
        duration_seconds=data.duration_seconds,
        album_id=data.album_id,
        creator_id=current_user.id,
    )

    return song_repository.create_song(db, song)


def get_song(db: Session, song_id: int):
    song = song_repository.get_song_by_id(db, song_id)

    if not song or not song.is_active:
        raise HTTPException(
            status_code=404,
            detail="Song not found",
        )

    return song


def get_songs(db: Session, skip: int = 0, limit: int = 10):
    return song_repository.get_all_songs(
        db,
        skip,
        limit,
    )


def get_my_songs(
    db: Session,
    current_user: User,
    skip: int = 0,
    limit: int = 10,
):
    return song_repository.get_songs_by_creator(
        db,
        current_user.id,
        skip,
        limit,
    )


def update_song(
    db: Session,
    song_id: int,
    data: SongUpdate,
    current_user: User,
):
    song = get_song(db, song_id)

    if song.creator_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own songs",
        )

    update_data = data.model_dump(exclude_unset=True)

    # Validate the new album if album_id is being changed.
    if "album_id" in update_data and update_data["album_id"] is not None:
        album = album_repository.get_album_by_id(
            db,
            update_data["album_id"],
        )

        if not album:
            raise HTTPException(
                status_code=404,
                detail="Album not found",
            )

        if album.creator_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You can only assign songs to your own albums",
            )

    for field, value in update_data.items():
        setattr(song, field, value)

    return song_repository.update_song(db, song)


def delete_song(
    db: Session,
    song_id: int,
    current_user: User,
):
    song = get_song(db, song_id)

    is_owner = song.creator_id == current_user.id
    is_admin = current_user.role == UserRole.ADMIN

    if not is_owner and not is_admin:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this song",
        )

    song_repository.deactivate_song(db, song)

    return {"message": "Song deactivated successfully"}