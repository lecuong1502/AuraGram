from fastapi import APIRouter, Depends, UploadFile, File
from src.core.dependencies import get_current_user
from src.models import User
from src.schemas.user import UserPublic, UpdateProfileRequest
from src.services import user as user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserPublic)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user.to_public()

@router.patch("/me", response_model=UserPublic)
async def update_me(
    data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
):
    updated = await user_service.update_profile(current_user, data)
    return updated.to_public()

@router.post("/me/avatar", response_model=UserPublic)
async def update_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    updated = await user_service.update_avatar(current_user, file)
    return updated.to_public()

@router.get("/{username}", response_model=UserPublic)
async def get_profile(username: str):
    user = await user_service.get_profile(username)
    return user.to_public()

@router.post("/{user_id}/follow", status_code=204)
async def follow(user_id: str, current_user: User = Depends(get_current_user)):
    await user_service.follow(current_user, user_id)

@router.delete("/{user_id}/follow", status_code=204)
async def unfollow(user_id: str, current_user: User = Depends(get_current_user)):
    await user_service.unfollow(current_user, user_id)

@router.get("/search", response_model=list[UserPublic])
async def search(q: str, current_user: User = Depends(get_current_user)):
    users = await user_service.search_users(q)
    return [u.to_public() for u in users]