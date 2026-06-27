from fastapi import HTTPException, status, UploadFile
from beanie import PydanticObjectId
from src.models import User, Follow
from src.schemas.user import UpdateProfileRequest
import cloudinary
import cloudinary.uploader

async def get_profile(username: str) -> User:
    user = await User.find_one(User.username == username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

async def update_profile(user: User, data: UpdateProfileRequest) -> User:
    if data.full_name is not None:
        user.full_name = data.full_name
    if data.bio is not None:
        user.bio = data.bio
    if data.is_private is not None:
        user.is_private = data.is_private
    await user.save()
    return user

async def update_avatar(user: User, file: UploadFile) -> User:
    # Delete old avatar from Cloudinary if exists
    if user.avatar_public_id:
        cloudinary.uploader.destroy(user.avatar_public_id)

    result = cloudinary.uploader.upload(
        file.file,
        folder="auragram/avatars",
        transformation={"width": 300, "height": 300, "crop": "fill"},
    )
    user.avatar_url = result["secure_url"]
    user.avatar_public_id = result["public_id"]
    await user.save()
    return user

async def follow(actor: User, target_id: str) -> None:
    target = await User.get(PydanticObjectId(target_id))
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if str(actor.id) == target_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot follow yourself")

    existing = await Follow.find_one(
        Follow.follower_id == actor.id,
        Follow.following_id == target.id,
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already following")

    status_val = "pending" if target.is_private else "accepted"
    await Follow(follower_id=actor.id, following_id=target.id, status=status_val).insert()

    if status_val == "accepted":
        # Update denormalized counters
        await actor.inc({User.following_count: 1})
        await target.inc({User.follower_count: 1})

async def unfollow(actor: User, target_id: str) -> None:
    target = await User.get(PydanticObjectId(target_id))
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    follow_doc = await Follow.find_one(
        Follow.follower_id == actor.id,
        Follow.following_id == target.id,
    )
    if not follow_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not following this user")

    await follow_doc.delete()

    if follow_doc.status == "accepted":
        await actor.inc({User.following_count: -1})
        await target.inc({User.follower_count: -1})

async def search_users(query: str, limit: int = 20) -> list[User]:
    return await User.find(
        {"$text": {"$search": query}},
        limit=limit,
    ).to_list()