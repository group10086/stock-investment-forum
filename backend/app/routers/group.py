"""群组路由"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.jwt_handler import get_current_user, get_optional_user
from app.services.group_service import GroupService

router = APIRouter(prefix="/api/groups", tags=["群组"])


@router.get("")
def get_groups(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """获取群组列表"""
    result = GroupService.get_groups(db, page, page_size)
    return {"data": result}


@router.post("")
def create_group(
    name: str,
    description: str = "",
    is_public: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建群组"""
    group = GroupService.create_group(db, current_user.id, name, description, is_public)
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
