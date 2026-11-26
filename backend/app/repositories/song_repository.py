from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.song import Song


def create_song(db: Session, song: Song) -> Song:
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


def get_song_by_id(db: Session, song_id: int):
    return db.scalar(
        select(Song).where(Song.id == song_id)
    )


def get_all_songs(db: Session, skip: int = 0, limit: int = 10):
    statement = (
        select(Song)
        .where(Song.is_active.is_(True))
        .order_by(Song.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


def get_songs_by_creator(
    db: Session,
    creator_id: int,
    skip: int = 0,
    limit: int = 10,
):
    statement = (
        select(Song)
        .where(
            Song.creator_id == creator_id,
            Song.is_active.is_(True),
        )
        .order_by(Song.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return db.scalars(statement).all()


def update_song(db: Session, song: Song) -> Song:
    db.commit()
    db.refresh(song)
    return song


def deactivate_song(db: Session, song: Song) -> Song:
    song.is_active = False
    db.commit()
    db.refresh(song)
    return song