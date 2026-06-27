from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from typing import Optional
from src.core.dependencies import get_current_user
from src.models import User
from src.schemas.post import PostOut, FeedResponse
from src.services import post as post_service

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/feed", response_model=FeedResponse)
async def get_feed(
    cursor: Optional[str] = Query(None),
    limit: int = Query(20, le=50),
    current_user: User = Depends(get_current_user),
):
    return await post_service.get_feed(current_user, cursor, limit)

@router.post("", response_model=PostOut, status_code=201)
async def create_post(
    caption: str = Form(default=""),
    files: list[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
):
    from src.schemas.post import PostCreateRequest
    data = PostCreateRequest(caption=caption)
    return await post_service.create_post(current_user, data, files)

@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: str):
    return await post_service.get_post(post_id)

@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_user),
):
    await post_service.delete_post(post_id, current_user)

@router.post("/{post_id}/like")
async def toggle_like(
    post_id: str,
    current_user: User = Depends(get_current_user),
):
    return await post_service.toggle_like(post_id, current_user)