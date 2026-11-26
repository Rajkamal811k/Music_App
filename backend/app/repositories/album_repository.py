from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.album import Album


def create_album(
    db: Session,
    album: Album
):

    db.add(album)

    db.commit()

    db.refresh(album)

    return album


def get_album_by_id(
    db: Session,
    album_id: int
):

    statement = select(Album).where(
        Album.id == album_id
    )

    return db.scalar(statement)


def get_all_albums(
    db: Session,
    skip: int = 0,
    limit: int = 10
):

    statement = (
        select(Album)
        .order_by(Album.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def get_albums_by_creator(
    db: Session,
    creator_id: int
):

    statement = (
        select(Album)
        .where(Album.creator_id == creator_id)
        .order_by(Album.created_at.desc())
    )

    return list(db.scalars(statement).all())


def update_album(
    db: Session,
    album: Album
):

    db.commit()

    db.refresh(album)

    return album


def delete_album(
    db: Session,
    album: Album
):

    db.delete(album)

    db.commit()