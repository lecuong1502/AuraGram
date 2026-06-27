from fastapi import APIRouter, Depends, Query
from src.core.dependencies import get_current_user
from src.models import User
from src.schemas.notification import NotificationListResponse
from src.services import notification as notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("", response_model=NotificationListResponse)
async def get_notifications(
    limit: int = Query(30, le=100),
    current_user: User = Depends(get_current_user),
):
    return await notification_service.get_notifications(current_user, limit)

@router.post("/read-all", status_code=204)
async def mark_all_read(current_user: User = Depends(get_current_user)):
    await notification_service.mark_all_read(current_user)