"""评论 Pydantic 数据模型"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    parent_id: Optional[int] = None


class CommentUserInfo(BaseModel):
    id: int
    nickname: str
    avatar: str

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    parent_id: Optional[int] = None
    content: str
    like_count: int
    is_liked: bool = False
    is_deleted: bool = False
    user: Optional[CommentUserInfo] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    list: List[CommentResponse]
    total: int
