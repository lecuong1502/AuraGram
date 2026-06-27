from pydantic import BaseModel
from typing import Optional

class NotificationOut(BaseModel):
    id: str
    actor_id: str
    type: str
    is_read: bool
    post_id: Optional[str]
    comment_id: Optional[str]
    created_at: str

class NotificationListResponse(BaseModel):
    notifications: list[NotificationOut]
    unread_count: int