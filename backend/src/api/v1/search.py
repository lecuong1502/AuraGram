from fastapi import APIRouter, Depends, Query
from typing import Optional
from src.core.dependencies import get_current_user
from src.models import User
from src.schemas.post import PostOut, FeedResponse
from src.schemas.user import UserPublic
from src.services import post as post_service, user as user_service

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/posts", response_model=FeedResponse)
async def search_posts(
    q: str = Query(..., min_length=1, description="Hashtag or keyword to search"),
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, le=50),
    current_user: User = Depends(get_current_user),
):
    """Search posts by hashtag (e.g. ?q=travel) or keyword in caption."""
    return await post_service.search_posts(q, cursor, limit)


@router.get("/users", response_model=list[UserPublic])
async def search_users(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, le=50),
    current_user: User = Depends(get_current_user),
):
    """Search users by username or full name."""
    users = await user_service.search_users(q, limit)
    return [u.to_public() for u in users]


@router.get("/explore", response_model=FeedResponse)
async def explore(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, le=50),
    current_user: User = Depends(get_current_user),
):
    """Global explore feed — most recent public posts."""
    return await post_service.get_explore_feed(cursor, limit)
