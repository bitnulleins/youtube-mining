from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class YTVideo(BaseModel):
    id: str
    title: str
    channel: str
    channel_id: str
    published_at: datetime
    rank: int
    tags: Optional[List[str]] = None
    category: int
    description: Optional[str] = None
    likes: Optional[int] = None
    dislikes: Optional[int] = None
    comments: Optional[int] = None
    views: int
    duration: int
    audio_language: Optional[str] = None
    text_language: Optional[str] = None
    caption: bool
    licensed_content: bool
    projection: str

