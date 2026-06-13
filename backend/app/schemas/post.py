"""帖子 Pydantic 数据模型"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    content: str = Field(..., min_length=10)
    summary: Optional[str] = ""
    category: Optional[str] = "other"
    tags: Optional[List[str]] = []
    images: Optional[List[str]] = []


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    content: Optional[str] = Field(None, min_length=10)
    summary: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    images: Optional[List[str]] = None


class PostUserInfo(BaseModel):
    id: int
    nickname: str
    avatar: str

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    summary: str
    category: str
    images: list
    tags: list
    is_top: bool
    is_essence: bool
    is_hot: bool
    view_count: int
    like_count: int
    comment_count: int
    bookmark_count: int
    is_liked: bool = False
    is_bookmarked: bool = False
    user: Optional[PostUserInfo] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PostListItem(BaseModel):
    id: int
    user_id: int
    title: str
    summary: str
    category: str
    images: list
    tags: list
    is_top: bool
    is_essence: bool
    is_hot: bool
    view_count: int
    like_count: int
    comment_count: int
    is_liked: bool = False
    is_bookmarked: bool = False
    user: Optional[PostUserInfo] = None
    created_at: datetime

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    list: List[PostListItem]
    total: int
    page: int
    page_size: int
    has_more: bool
