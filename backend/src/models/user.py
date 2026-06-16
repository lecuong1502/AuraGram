from datetime import datetime, timezone
from typing import Optional, Annotated
from beanie import Document, Indexed
from pydantic import EmailStr, Field
import bcrypt


class User(Document):
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[EmailStr, Indexed(unique=True)]
    password_hash: str = Field(exclude=True)  # never returned in responses
    full_name: Optional[str] = None
    bio: str = ""
    avatar_url: str = ""
    avatar_public_id: str = Field(default="", exclude=True)  # Cloudinary public_id

    is_verified: bool = False
    is_private: bool = False

    # Denormalized counters — avoids COUNT(*) on every profile load
    post_count: int = 0
    follower_count: int = 0
    following_count: int = 0

    # CLIP embedding of the avatar — used for semantic search (Phase 3)
    clip_embedding: Optional[list[float]] = Field(default=None, exclude=True)

    # Refresh tokens — stored to support revocation
    refresh_tokens: list[str] = Field(default_factory=list, exclude=True)

    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

    class Settings:
        name = "users"
        indexes = [
            "username",
            "email",
            [("full_name", "text"), ("username", "text")],  # full-text search
        ]

    # Helpers

    def set_password(self, plaintext: str) -> None:
        self.password_hash = bcrypt.hashpw(
            plaintext.encode(), bcrypt.gensalt(rounds=12)
        ).decode()

    def verify_password(self, plaintext: str) -> bool:
        return bcrypt.checkpw(plaintext.encode(), self.password_hash.encode())

    def to_public(self) -> dict:
        return {
            "id": str(self.id),
            "username": self.username,
            "full_name": self.full_name,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "is_verified": self.is_verified,
            "is_private": self.is_private,
            "post_count": self.post_count,
            "follower_count": self.follower_count,
            "following_count": self.following_count,
            "created_at": self.created_at.isoformat(),
        }