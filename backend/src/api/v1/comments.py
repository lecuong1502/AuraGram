from fastapi import APIRouter, Depends, Query
from src.core.dependencies import get_current_user
from src.models import User
from src.schemas.comment import CommentOut, CommentCreateRequest, ReplyCreateRequest
from src.services import comment as comment_service

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])

@router.get("", response_model=list[CommentOut])
async def list_comments(
    post_id: str,
    limit: int = Query(20, le=50),
    skip: int = Query(0),
):
    return await comment_service.list_comments(post_id, limit, skip)

@router.post("", response_model=CommentOut, status_code=201)
async def add_comment(
    post_id: str,
    data: CommentCreateRequest,
    current_user: User = Depends(get_current_user),
):
    return await comment_service.add_comment(post_id, current_user, data)

@router.delete("/{comment_id}", status_code=204)
async def delete_comment(
    comment_id: str,
    current_user: User = Depends(get_current_user),
):
    await comment_service.delete_comment(comment_id, current_user)

@router.post("/{comment_id}/replies", response_model=CommentOut, status_code=201)
async def add_reply(
    comment_id: str,
    data: ReplyCreateRequest,
    current_user: User = Depends(get_current_user),
):
    return await comment_service.add_reply(comment_id, current_user, data)