from typing import Optional, List

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from app.models.song import Song


def create_song(db: Session, song: Song) -> Song:

    db.add(song)
    db.commit()
    db.refresh(song)

    return song


def get_all_songs(db: Session) -> List[Song]:

    statement = select(Song).order_by(Song.created_at.desc())

    return list(db.scalars(statement).all())


def get_song_by_id(db: Session, song_id: int) -> Optional[Song]:

    statement = select(Song).where(Song.id == song_id)

    return db.scalar(statement)


def get_songs_by_user(db: Session, user_id: int) -> List[Song]:

    statement = select(Song).where(
        Song.uploaded_by == user_id
    ).order_by(Song.created_at.desc())

    return list(db.scalars(statement).all())


def search_songs(db: Session, query: str) -> List[Song]:

    pattern = f"%{query}%"

    statement = select(Song).where(
        or_(
            Song.title.ilike(pattern),
            Song.artist.ilike(pattern),
            Song.album.ilike(pattern),
            Song.genre.ilike(pattern)
        )
    ).order_by(Song.created_at.desc())

    return list(db.scalars(statement).all())


def delete_song(db: Session, song: Song) -> None:

    db.delete(song)
    db.commit()
