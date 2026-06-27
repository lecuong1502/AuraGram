from beanie import PydanticObjectId
from src.models import Notification, User
from src.schemas.notification import NotificationOut, NotificationListResponse

def _to_out(n: Notification) -> NotificationOut:
    return NotificationOut(
        id=str(n.id),
        actor_id=str(n.actor_id),
        type=n.type,
        is_read=n.is_read,
        post_id=str(n.post_id) if n.post_id else None,
        comment_id=str(n.comment_id) if n.comment_id else None,
        created_at=n.created_at.isoformat(),
    )

async def get_notifications(user: User, limit: int = 30) -> NotificationListResponse:
    notifications = await Notification.find(
        Notification.recipient_id == user.id,
    ).sort(-Notification.created_at).limit(limit).to_list()

    unread_count = await Notification.find(
        Notification.recipient_id == user.id,
        Notification.is_read == False,
    ).count()

    return NotificationListResponse(
        notifications=[_to_out(n) for n in notifications],
        unread_count=unread_count,
    )

async def mark_all_read(user: User) -> None:
    await Notification.find(
        Notification.recipient_id == user.id,
        Notification.is_read == False,
    ).update({"$set": {"is_read": True}})

async def push_notification(
    recipient_id: PydanticObjectId,
    actor_id: PydanticObjectId,
    type: str,
    post_id: PydanticObjectId | None = None,
    comment_id: PydanticObjectId | None = None,
) -> None:
    # Skip self-notifications
    if recipient_id == actor_id:
        return

    notification = Notification(
        recipient_id=recipient_id,
        actor_id=actor_id,
        type=type,
        post_id=post_id,
        comment_id=comment_id,
    )
    # unique index on (recipient, actor, type, post) handles deduplication
    try:
        await notification.insert()
    except Exception:
        pass