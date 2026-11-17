from typing import Optional, List

from pydantic import BaseModel


class SongResponse(BaseModel):

    id: int
    title: str
    artist: str
    album: Optional[str] = ""
    genre: Optional[str] = ""
    duration: int
    file_path: str
    cover_image_path: Optional[str] = None
    uploaded_by: int

    model_config = {
        "from_attributes": True
    }


class SongListResponse(BaseModel):

    songs: List[SongResponse]
    total: int
