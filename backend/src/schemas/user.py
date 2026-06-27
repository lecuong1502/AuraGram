from pydantic import BaseModel

class UserPublic(BaseModel):
    id: str
    username: str
    full_name: str | None
    bio: str
    avatar_url: str
    is_verified: bool
    is_private: bool
    post_count: int
    follower_count: int
    following_count: int
    created_at: str

class UpdateProfileRequest(BaseModel):
    full_name: str | None = None
    bio: str | None = None
    is_private: bool | None = None