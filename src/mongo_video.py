from pydantic import BaseModel
import datetime as dt
from typing import Any, List, Optional

class MongoVideo(BaseModel):
    video_id: str
    created: str
    published_at: str
    modified_at: Optional[str] = None
    channel: str
    channel_id: str
    rank: List[Any]
    title: List[Any]
    tags: List[Any]
    category: int
    description: str
    likes: List[Any]
    dislikes: List[Any]
    comments: List[Any]
    views: List[Any]
    duration: int
    audio_language: Optional[str] = None
    text_language: Optional[str] = None
    caption: bool
    licensed_content: bool
    projection: str

    class Config:
        fields = {'video_id': '_id'}