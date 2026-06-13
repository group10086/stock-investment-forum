"""私信 Pydantic 数据模型"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    receiver_id: int
    content: str = Field(..., min_length=1, max_length=2000)


class MessageUserInfo(BaseModel):
    id: int
    nickname: str
    avatar: str

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    is_read: bool
    sender: Optional[MessageUserInfo] = None
    receiver: Optional[MessageUserInfo] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    user: MessageUserInfo
    last_message: str
    last_time: datetime
    unread_count: int
