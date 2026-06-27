from pydantic import BaseModel, Field
from typing import Optional

class ReplyOut(BaseModel):
    id: str
    author_id: str
    content: str
    like_count: int
    mention_id: Optional[str]
    created_at: str

class CommentOut(BaseModel):
    id: str
    post_id: str
    author_id: str
    content: str
    like_count: int
    replies: list[ReplyOut]
    is_pinned: bool
    created_at: str

class CommentCreateRequest(BaseModel):
    content: str = Field(max_length=1000)

class ReplyCreateRequest(BaseModel):
    content: str = Field(max_length=1000)
    mention_id: Optional[str] = None