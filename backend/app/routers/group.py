"""群组路由"""

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.group import Group, GroupMember
from app.utils.jwt_handler import get_current_user, get_optional_user
from app.services.group_service import GroupService
from pydantic import BaseModel

router = APIRouter(prefix="/api/groups", tags=["群组"])


class GroupCreateBody(BaseModel):
    name: str
    description: str = ""
    is_public: bool = True


@router.get("")
def get_groups(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    my: bool = Query(False),
    current_user: User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取群组列表"""
    current_user_id = current_user.id if current_user else None
    if my and current_user_id:
        result = GroupService.get_my_groups(db, current_user_id, page, page_size)
    else:
        result = GroupService.get_groups(db, page, page_size)
    return {"data": result}


@router.post("")
def create_group(
    data: GroupCreateBody,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建群组"""
    group = GroupService.create_group(db, current_user.id, data.name, data.description, data.is_public)
    return {"message": "创建成功", "data": {"id": group.id, "name": group.name}}


@router.get("/{group_id}")
def get_group_detail(
    group_id: int,
    current_user: User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取群组详情"""
    current_user_id = current_user.id if current_user else None
    result = GroupService.get_group_detail(db, group_id, current_user_id)
    return {"data": result}


@router.post("/{group_id}/join")
def join_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """加入群组"""
    GroupService.join_group(db, group_id, current_user.id)
    return {"message": "已加入群组"}


@router.delete("/{group_id}/leave")
def leave_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """退出群组"""
    GroupService.leave_group(db, group_id, current_user.id)
    return {"message": "已退出群组"}


# ========== 群组消息 ==========

from app.models.group_message import GroupMessage


class GroupMsgCreate(BaseModel):
    content: str


@router.get("/{group_id}/messages")
def get_group_messages(
    group_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取群组消息"""
    from app.utils.pagination import paginate

    query = db.query(GroupMessage).filter(
        GroupMessage.group_id == group_id
    ).order_by(GroupMessage.created_at.asc())

    items, total, has_more = paginate(query, page, page_size)

    msg_list = []
    for msg in items:
        user = db.query(User).filter(User.id == msg.user_id).first()
        msg_list.append({
            "id": msg.id,
            "user_id": msg.user_id,
            "content": msg.content,
            "user": {
                "id": user.id if user else None,
                "nickname": user.nickname if user else "已注销",
                "avatar": user.avatar if user else "",
            },
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        })

    return {"data": {"list": msg_list, "total": total, "has_more": has_more}}


@router.post("/{group_id}/messages")
def send_group_message(
    group_id: int,
    data: GroupMsgCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送群组消息"""
    # 检查是否群成员
    member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == current_user.id
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="请先加入群组")

    msg = GroupMessage(
        group_id=group_id,
        user_id=current_user.id,
        content=data.content,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    return {
        "message": "发送成功",
        "data": {
            "id": msg.id,
            "user_id": msg.user_id,
            "content": msg.content,
            "user": {
                "id": current_user.id,
                "nickname": current_user.nickname,
                "avatar": current_user.avatar,
            },
            "created_at": msg.created_at.isoformat(),
        }
    }
