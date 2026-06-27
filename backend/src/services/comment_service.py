from fastapi import HTTPException, status
from beanie import PydanticObjectId
from src.models import Post, Comment, User
from src.models.comment import Reply
from src.schemas.comment import CommentCreateRequest, CommentOut, ReplyCreateRequest

def _reply_to_out(r: Reply) -> dict:
    return {
        "id": str(r.id),
        "author_id": str(r.author_id),
        "content": r.content,
        "like_count": r.like_count,
        "mention_id": str(r.mention_id) if r.mention_id else None,
        "created_at": r.created_at.isoformat(),
    }

def _comment_to_out(c: Comment) -> CommentOut:
    return CommentOut(
        id=str(c.id),
        post_id=str(c.post_id),
        author_id=str(c.author_id),
        content=c.content,
        like_count=c.like_count,
        replies=[_reply_to_out(r) for r in c.replies if not r.is_deleted],
        is_pinned=c.is_pinned,
        created_at=c.created_at.isoformat(),
    )

async def list_comments(post_id: str, limit: int = 20, skip: int = 0) -> list[CommentOut]:
    comments = await Comment.find(
        Comment.post_id == PydanticObjectId(post_id),
        Comment.is_deleted == False,
    ).sort([("is_pinned", -1), ("created_at", 1)]).skip(skip).limit(limit).to_list()

    return [_comment_to_out(c) for c in comments]

async def add_comment(post_id: str, user: User, data: CommentCreateRequest) -> CommentOut:
    post = await Post.get(PydanticObjectId(post_id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comment = Comment(
        post_id=post.id,
        author_id=user.id,
        content=data.content,
    )
    await comment.insert()
    await post.inc({Post.comment_count: 1})
    return _comment_to_out(comment)

async def delete_comment(comment_id: str, user: User) -> None:
    comment = await Comment.get(PydanticObjectId(comment_id))
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    if str(comment.author_id) != str(user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your comment")

    comment.is_deleted = True
    await comment.save()

    post = await Post.get(comment.post_id)
    if post:
        await post.inc({Post.comment_count: -1})

async def add_reply(comment_id: str, user: User, data: ReplyCreateRequest) -> CommentOut:
    comment = await Comment.get(PydanticObjectId(comment_id))
    if not comment or comment.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    reply = Reply(
        author_id=user.id,
        content=data.content,
        mention_id=PydanticObjectId(data.mention_id) if data.mention_id else None,
    )
    comment.replies.append(reply)
    await comment.save()
    return _comment_to_out(comment)