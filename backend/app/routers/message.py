"""私信路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.message import MessageCreate
from app.services.message_service import MessageService
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/messages", tags=["私信"])


@router.get("/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取未读消息数"""
    count = MessageService.get_unread_count(db, current_user.id)
    return {"data": {"count": count}}


@router.get("/conversations")
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取会话列表"""
    conversations = MessageService.get_conversations(db, current_user.id)
    return {"data": conversations}


@router.get("/{user_id}")
def get_messages(
    user_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取与某用户的私信"""
    result = MessageService.get_messages(db, current_user.id, user_id, page, page_size)
    return {"data": result}


@router.post("")
def send_message(
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送私信"""
    message = MessageService.send_message(db, current_user.id, data)
    return {"message": "发送成功"}
