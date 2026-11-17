import os
import uuid

from fastapi import HTTPException, UploadFile, status

from sqlalchemy.orm import Session

from app.models.song import Song
from app.models.enums import UserRole
from app.repositories import song_repository


UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
SONGS_DIR = os.path.join(UPLOAD_DIR, "songs")
COVERS_DIR = os.path.join(UPLOAD_DIR, "covers")

ALLOWED_AUDIO_TYPES = {
    "audio/mpeg", "audio/mp3", "audio/wav", "audio/ogg",
    "audio/flac", "audio/aac", "audio/x-wav", "audio/webm",
    "audio/mp4", "audio/x-m4a",
}


def _ensure_dirs():
    os.makedirs(SONGS_DIR, exist_ok=True)
    os.makedirs(COVERS_DIR, exist_ok=True)


def upload_song(
    db: Session,
    title: str,
    artist: str,
    album: str,
    genre: str,
    file: UploadFile,
    user_id: int,
    cover: UploadFile = None
) -> Song:

    _ensure_dirs()

    # Validate file type
    content_type = file.content_type or ""
    if content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid audio file type: {content_type}. Allowed: mp3, wav, ogg, flac, aac, webm, m4a"
        )

    # Save audio file
    ext = os.path.splitext(file.filename or "audio.mp3")[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(SONGS_DIR, unique_name)

    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    # Save cover image if provided
    cover_path = None
    if cover and cover.filename:
        cover_ext = os.path.splitext(cover.filename)[1]
        cover_name = f"{uuid.uuid4().hex}{cover_ext}"
        cover_full = os.path.join(COVERS_DIR, cover_name)
        with open(cover_full, "wb") as f:
            f.write(cover.file.read())
        cover_path = f"uploads/covers/{cover_name}"

    # Estimate duration from file size (rough: ~16KB per second for 128kbps mp3)
    file_size = len(content)
    estimated_duration = max(1, file_size // 16000)

    song = Song(
        title=title,
        artist=artist,
        album=album or "",
        genre=genre or "",
        duration=estimated_duration,
        file_path=f"uploads/songs/{unique_name}",
        cover_image_path=cover_path,
        uploaded_by=user_id
    )

    try:
        return song_repository.create_song(db, song)
    except Exception:
        # Clean up file if DB insert fails
        if os.path.exists(file_path):
            os.remove(file_path)
        db.rollback()
        raise


def get_all_songs(db: Session):
    return song_repository.get_all_songs(db)


def get_song(db: Session, song_id: int):

    song = song_repository.get_song_by_id(db, song_id)

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )

    return song


def search(db: Session, query: str):

    if not query or not query.strip():
        return song_repository.get_all_songs(db)

    return song_repository.search_songs(db, query.strip())


def delete_song(db: Session, song_id: int, current_user):

    song = song_repository.get_song_by_id(db, song_id)

    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )

    if song.uploaded_by != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this song"
        )

    # Delete file from disk
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    full_path = os.path.join(base_dir, song.file_path)
    if os.path.exists(full_path):
        os.remove(full_path)

    if song.cover_image_path:
        cover_full = os.path.join(base_dir, song.cover_image_path)
        if os.path.exists(cover_full):
            os.remove(cover_full)

    song_repository.delete_song(db, song)

    return {"detail": "Song deleted successfully"}
