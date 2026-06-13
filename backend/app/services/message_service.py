"""私信服务"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc

from app.models.user import User
from app.models.message import Message
from app.schemas.message import MessageCreate


class MessageService:
    """私信服务"""

    @staticmethod
    def send_message(db: Session, sender_id: int, data: MessageCreate) -> Message:
        """发送私�?""
        # 验证接收者存�?
        receiver = db.query(User).filter(User.id == data.receiver_id).first()
        if not receiver:
            raise HTTPException(status_code=404, detail="接收者不存在")

        if sender_id == data.receiver_id:
            raise HTTPException(status_code=400, detail="不能给自己发私信")

        # 检查接收者是否允许私�?
        if not receiver.allow_messages:
            raise HTTPException(status_code=403, detail="该用户不允许接收私信")

        message = Message(
            sender_id=sender_id,
            receiver_id=data.receiver_id,
            content=data.content,
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @staticmethod
    def get_messages(db: Session, user_id: int, other_user_id: int, page: int = 1, page_size: int = 50) -> dict:
        """获取与某用户的私信列�?""
        from app.utils.pagination import paginate

        query = db.query(Message).filter(
            or_(
                and_(Message.sender_id == user_id, Message.receiver_id == other_user_id),
                and_(Message.sender_id == other_user_id, Message.receiver_id == user_id)
            )
        ).order_by(Message.created_at.asc())

        items, total, has_more = paginate(query, page, page_size)

        # 标记为已�?
        unread = db.query(Message).filter(
            Message.receiver_id == user_id,
            Message.sender_id == other_user_id,
            Message.is_read == False
        ).all()
        for msg in unread:
            msg.is_read = True
        db.commit()

        message_list = []
        for msg in items:
            sender = db.query(User).filter(User.id == msg.sender_id).first()
            message_list.append({
                "id": msg.id,
                "sender_id": msg.sender_id,
                "receiver_id": msg.receiver_id,
                "content": msg.content,
                "is_read": msg.is_read,
                "is_mine": msg.sender_id == user_id,
                "user": {
                    "id": sender.id if sender else None,
                    "nickname": sender.nickname if sender else "已注销",
                    "avatar": sender.avatar if sender else "",
                },
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
            })

        return {"list": message_list, "total": total, "has_more": has_more}

    @staticmethod
    def get_unread_count(db: Session, user_id: int) -> int:
        """获取未读消息�?""
        return db.query(Message).filter(
            Message.receiver_id == user_id,
            Message.is_read == False
        ).count()

    @staticmethod
    def get_conversations(db: Session, user_id: int) -> list:
        """获取会话列表"""
        # 找出所有有消息交流的用�?
        from sqlalchemy import func, text

        subquery = db.query(
            func.max(Message.id).label("max_id")
        ).filter(
            or_(Message.sender_id == user_id, Message.receiver_id == user_id)
        ).group_by(
            func.least(Message.sender_id, Message.receiver_id),
            func.greatest(Message.sender_id, Message.receiver_id)
        ).subquery()

        latest_messages = db.query(Message).filter(
            Message.id.in_(db.query(subquery.c.max_id))
        ).order_by(Message.created_at.desc()).all()

        conversations = []
        for msg in latest_messages:
            other_user_id = msg.receiver_id if msg.sender_id == user_id else msg.sender_id
            other_user = db.query(User).filter(User.id == other_user_id).first()
            if not other_user:
                continue

            unread = db.query(Message).filter(
                Message.receiver_id == user_id,
                Message.sender_id == other_user_id,
                Message.is_read == False
            ).count()

            conversations.append({
                "user": {
                    "id": other_user.id,
                    "nickname": other_user.nickname,
                    "avatar": other_user.avatar,
                },
                "last_message": msg.content[:50] + "..." if len(msg.content) > 50 else msg.content,
                "last_time": msg.created_at.isoformat() if msg.created_at else None,
                "unread_count": unread,
            })

        return conversations
