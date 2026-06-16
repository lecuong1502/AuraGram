from datetime import datetime, timezone
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Reply(BaseModel):
    """
    Sub-document for replies — embedded because only 1 level deep (like Instagram),
    and the number of replies on a single comment is practically small.
    """

    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    author_id: PydanticObjectId

    content: str = Field(max_length=1000)
    like_count: int = 0

    # @mention target — the person being replied to
    mention_id: Optional[PydanticObjectId] = None

    is_deleted: bool = False
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))


class Comment(Document):
    post_id: PydanticObjectId
    author_id: PydanticObjectId

    content: str = Field(max_length=1000)
    like_count: int = 0

    # Embedded replies — max 1 level deep
    replies: list[Reply] = Field(default_factory=list)

    is_deleted: bool = False
    is_pinned: bool = False  # pinned by post author

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "comments"
        indexes = [
            # Load comments for a post, pinned first then by time
            [("post_id", 1), ("is_pinned", -1), ("created_at", 1)],
            # "All comments by user" — profile activity
            [("author_id", 1), ("created_at", -1)],
        ]