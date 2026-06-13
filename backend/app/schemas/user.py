"""用户 Pydantic 数据模型"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, max_length=20)
    bio: Optional[str] = Field(None, max_length=200)
    avatar: Optional[str] = None
    investment_preference: Optional[List[str]] = None
    github: Optional[str] = None
    email_public: Optional[bool] = None
    allow_messages: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    nickname: str
    avatar: str
    bio: str
    investment_preference: list
    github: str
    email_public: bool
    allow_messages: bool
    is_verified: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    id: int
    username: str
    nickname: str
    avatar: str
    bio: str
    investment_preference: list
    github: str
    is_verified: bool
    is_following: bool = False
    post_count: int = 0
    following_count: int = 0
    follower_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True
