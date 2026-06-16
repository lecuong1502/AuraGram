from datetime import datetime, timezone
from typing import Literal
from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import IndexModel, ASCENDING


class Follow(Document):
    """
    One document = one directed edge: follower → following.
    Separate collection instead of embedding an array in User, for easier
    bidirectional queries and no document size limits at scale.
    """

    follower_id: PydanticObjectId
    following_id: PydanticObjectId

    # "pending" when target account is private — awaiting approval
    status: Literal["accepted", "pending"] = "accepted"

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "follows"
        indexes = [
            # Unique constraint: each pair can only exist once
            IndexModel(
                [("follower_id", ASCENDING), ("following_id", ASCENDING)],
                unique=True,
            ),
            # "List of users I am following" — used in feed query
            [("follower_id", 1), ("status", 1)],
            # "List of my followers"
            [("following_id", 1), ("status", 1)],
        ]