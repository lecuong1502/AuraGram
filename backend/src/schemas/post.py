from pydantic import BaseModel, Field
from typing import Optional

class MediaItemOut(BaseModel):
    url: str
    width: Optional[int] = None
    height: Optional[int] = None
    detected_tags: list[str] = []

class PostCreateRequest(BaseModel):
    caption: str = Field(default="", max_length=2200)
    location_name: str = ""
    # media is handled separately as multipart file upload

class PostOut(BaseModel):
    id: str
    author_id: str
    caption: str
    media: list[MediaItemOut]
    tags: list[str]
    hashtags: list[str]
    ai_caption: str
    like_count: int
    comment_count: int
    is_archived: bool
    created_at: str

class FeedResponse(BaseModel):
    posts: list[PostOut]
    next_cursor: Optional[str] = None  # cursor-based pagination
    has_more: bool