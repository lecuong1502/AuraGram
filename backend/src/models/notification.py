from datetime import datetime, timezone
from typing import Literal, Optional
from beanie import Document, PydanticObjectId
from pydantic import Field
from pymongo import IndexModel, ASCENDING, DESCENDING


NotificationType = Literal[
    "like",        # someone liked your post
    "comment",     # someone commented on your post
    "reply",       # someone replied to your comment
    "follow",      # someone followed you
    "follow_req",  # someone requested to follow (private account)
    "mention",     # someone mentioned you in a caption/comment
]


class Notification(Document):
    recipient_id: PydanticObjectId   # the recipient
    actor_id: PydanticObjectId       # the user who triggered the action

    type: NotificationType
    is_read: bool = False

    # Reference to the related post/comment (nullable)
    post_id: Optional[PydanticObjectId] = None
    comment_id: Optional[PydanticObjectId] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "notifications"
        indexes = [
            # Load notification bell, newest first
            [("recipient_id", 1), ("created_at", -1)],
            # Fast unread count
            [("recipient_id", 1), ("is_read", 1)],
            # TTL — auto-delete notifications older than 90 days, no cron job needed
            IndexModel(
                [("created_at", ASCENDING)],
                expireAfterSeconds=60 * 60 * 24 * 90,
            ),
            # Prevent duplicates (e.g., like → unlike → like again creates 2 notifications)
            IndexModel(
                [
                    ("recipient_id", ASCENDING),
                    ("actor_id", ASCENDING),
                    ("type", ASCENDING),
                    ("post_id", ASCENDING),
                ],
                unique=True,
                sparse=True,
            ),
        ]