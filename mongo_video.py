from pydantic import BaseModel
import datetime as dt
from typing import Any, List, Optional


class VersionEntry(BaseModel):
    version: int
    date: str
    value: Any = None


class MongoVideo(BaseModel):
    video_id: str
    created: str
    published_at: str
    channel: str
    channel_id: str
    rank: List[VersionEntry]
    title: List[VersionEntry]
    tags: List[VersionEntry]
    category: int
    description: List[VersionEntry]
    likes: List[VersionEntry]
    dislikes: List[VersionEntry]
    comments: List[VersionEntry]
    views: List[VersionEntry]
    duration: int
    audio_language: Optional[str] = None
    text_language: Optional[str] = None
    caption: bool
    licensed_content: bool
    projection: str

    class Config:
        fields = {'video_id': '_id'}