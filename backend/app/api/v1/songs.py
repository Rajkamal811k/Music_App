import os
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.database.connection import get_db

from app.schemas.song import SongResponse, SongListResponse

from app.services import song_service

from app.core.dependencies import get_current_user, require_role

from app.models.enums import UserRole


router = APIRouter(
    prefix="/songs",
    tags=["Songs"]
)


@router.post(
    "/upload",
    response_model=SongResponse,
    status_code=status.HTTP_201_CREATED
)
def upload_song(
    title: str = Form(...),
    artist: str = Form(...),
    album: str = Form(""),
    genre: str = Form(""),
    file: UploadFile = File(...),
    cover: Optional[UploadFile] = File(None),
    current_user=Depends(require_role(UserRole.CREATOR, UserRole.ADMIN)),
    db: Session = Depends(get_db)
):

    return song_service.upload_song(
        db=db,
        title=title,
        artist=artist,
        album=album,
        genre=genre,
        file=file,
        user_id=current_user.id,
        cover=cover
    )


@router.get(
    "",
    response_model=SongListResponse
)
def list_songs(
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    if search:
        songs = song_service.search(db, search)
    else:
        songs = song_service.get_all_songs(db)

    return {
        "songs": songs,
        "total": len(songs)
    }


@router.get(
    "/{song_id}",
    response_model=SongResponse
)
def get_song(
    song_id: int,
    db: Session = Depends(get_db)
):

    return song_service.get_song(db, song_id)


@router.get(
    "/{song_id}/stream"
)
def stream_song(
    song_id: int,
    db: Session = Depends(get_db)
):

    song = song_service.get_song(db, song_id)

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    full_path = os.path.join(base_dir, song.file_path)

    if not os.path.exists(full_path):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Audio file not found on disk"
        )

    # Determine media type
    ext = os.path.splitext(full_path)[1].lower()
    media_types = {
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".flac": "audio/flac",
        ".aac": "audio/aac",
        ".m4a": "audio/mp4",
        ".webm": "audio/webm",
    }
    media_type = media_types.get(ext, "audio/mpeg")

    return FileResponse(
        full_path,
        media_type=media_type,
        filename=f"{song.title}{ext}"
    )


@router.delete(
    "/{song_id}",
    status_code=status.HTTP_200_OK
)
def delete_song(
    song_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return song_service.delete_song(db, song_id, current_user)
