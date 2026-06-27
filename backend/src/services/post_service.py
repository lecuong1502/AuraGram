from fastapi import HTTPException, UploadFile, status
from beanie import PydanticObjectId
from beanie.operators import In
from src.models import User, Post, Follow, Like
from src.models.post import MediaItem
from src.schemas.post import PostCreateRequest, PostOut, FeedResponse
from src.services.upload_service import upload_image, delete_image
from datetime import datetime

def _to_out(post: Post) -> PostOut:
    return PostOut(
        id=str(post.id),
        author_id=str(post.author_id),
        caption=post.caption,
        media=[
            {"url": m.url, "width": m.width, "height": m.height, "detected_tags": m.detected_tags}
            for m in post.media
        ],
        tags=post.tags,
        hashtags=post.hashtags,
        ai_caption=post.ai_caption,
        like_count=post.like_count,
        comment_count=post.comment_count,
        is_archived=post.is_archived,
        created_at=post.created_at.isoformat(),
    )

async def create_post(
    author: User,
    data: PostCreateRequest,
    files: list[UploadFile],
) -> PostOut:
    if not files or len(files) > 10:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A post requires between 1 and 10 images",
        )

    # Upload all images to Cloudinary
    media_items = []
    for file in files:
        uploaded = await upload_image(file)
        media_items.append(MediaItem(**uploaded))

    # Extract hashtags from caption
    hashtags = [word[1:].lower() for word in data.caption.split() if word.startswith("#")]

    post = Post(
        author_id=author.id,
        caption=data.caption,
        media=media_items,
        hashtags=hashtags,
    )
    await post.insert()

    # Update denormalized post counter on User
    await author.inc({User.post_count: 1})

    return _to_out(post)

async def get_post(post_id: str) -> PostOut:
    post = await Post.get(PydanticObjectId(post_id))
    if not post or post.is_archived:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return _to_out(post)

async def delete_post(post_id: str, current_user: User) -> None:
    post = await Post.get(PydanticObjectId(post_id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    if str(post.author_id) != str(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your post")

    # Delete all images from Cloudinary
    for media in post.media:
        await delete_image(media.public_id)

    await post.delete()
    await current_user.inc({User.post_count: -1})

async def get_feed(current_user: User, cursor: str | None, limit: int = 20) -> FeedResponse:
    # Get IDs of users that current_user follows
    follows = await Follow.find(
        Follow.follower_id == current_user.id,
        Follow.status == "accepted",
    ).to_list()
    following_ids = [f.following_id for f in follows] + [current_user.id]

    query = Post.find(
        In(Post.author_id, following_ids),
        Post.is_archived == False,
    )

    # Cursor-based pagination — cursor is the created_at of the last seen post
    if cursor:
        query = query.find(Post.created_at < datetime.fromisoformat(cursor))

    posts = await query.sort(-Post.created_at).limit(limit + 1).to_list()

    has_more = len(posts) > limit
    posts = posts[:limit]
    next_cursor = posts[-1].created_at.isoformat() if has_more and posts else None

    return FeedResponse(
        posts=[_to_out(p) for p in posts],
        next_cursor=next_cursor,
        has_more=has_more,
    )

async def toggle_like(post_id: str, user: User) -> dict:
    post = await Post.get(PydanticObjectId(post_id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    existing = await Like.find_one(Like.user_id == user.id, Like.post_id == post.id)

    if existing:
        await existing.delete()
        await post.inc({Post.like_count: -1})
        await post.sync()
        return {"liked": False, "like_count": post.like_count}
    else:
        await Like(user_id=user.id, post_id=post.id).insert()
        await post.inc({Post.like_count: 1})
        await post.sync()
        return {"liked": True, "like_count": post.like_count}