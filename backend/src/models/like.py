from datetime import datetime, timezone
from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import IndexModel, ASCENDING, DESCENDING


class Like(Document):
    """
    Separate collection instead of embedding an array in Post.
    A viral post can have millions of likes — embedding would exceed the 16MB document limit.
    A separate collection also allows easy "which posts has the user liked" queries.
    """

    user_id: PydanticObjectId
    post_id: PydanticObjectId

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "likes"
        indexes = [
            # Unique: each user can only like a post once
            IndexModel(
                [("user_id", ASCENDING), ("post_id", ASCENDING)],
                unique=True,
            ),
            # "All likes for this post" — used when listing who liked
            [("post_id", 1), ("created_at", -1)],
            # "All posts liked by user" — profile "liked posts" tab
            [("user_id", 1), ("created_at", -1)],
        ]