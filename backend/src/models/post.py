from datetime import datetime, timezone
from typing import Optional
from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field


class MediaItem(BaseModel):
    """Sub-document for each image in a carousel (max 10)."""

    url: str
    public_id: str  # Cloudinary public_id — used for image deletion
    width: Optional[int] = None
    height: Optional[int] = None

    # AI fields (Phase 3)
    detected_tags: list[str] = Field(default_factory=list)  # YOLOv8 output
    clip_embedding: Optional[list[float]] = Field(default=None, exclude=True)


class GeoPoint(BaseModel):
    type: str = "Point"
    coordinates: list[float] = Field(default_factory=list)  # [lng, lat]


class Location(BaseModel):
    name: str = ""
    coordinates: Optional[GeoPoint] = None


class Post(Document):
    author_id: PydanticObjectId
    caption: str = Field(default="", max_length=2200)

    # Multiple images — validate 1-10 images at service layer
    media: list[MediaItem] = Field(default_factory=list)

    # Union of all detected_tags across all images in the post
    tags: list[str] = Field(default_factory=list)
    hashtags: list[str] = Field(default_factory=list)

    # AI-generated caption — distinguished from user-entered caption (Phase 2)
    ai_caption: str = ""

    # Denormalized counters
    like_count: int = 0
    comment_count: int = 0

    is_archived: bool = False
    location: Optional[Location] = None

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "posts"
        indexes = [
            [("author_id", 1), ("created_at", -1)],   # profile grid
            [("created_at", -1)],                       # global feed
            "tags",
            "hashtags",
            [("is_archived", 1), ("created_at", -1)],
            [("caption", "text"), ("ai_caption", "text")],  # text search fallback
            [("location.coordinates", "2dsphere")],
        ]