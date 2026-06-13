"""用户路由 - 用户系统"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse, UserDetailResponse
from app.services.user_service import UserService
from app.utils.jwt_handler import get_current_user, get_optional_user

router = APIRouter(prefix="/api/user", tags=["用户"])


@router.get("/info")
def get_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户信息"""
    user = UserService.get_user_info(db, current_user.id)
    return {"data": UserResponse.model_validate(user)}


@router.put("/info")
def update_user_info(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    user = UserService.update_user_info(db, current_user.id, data)
    return {"message": "更新成功", "data": UserResponse.model_validate(user)}


@router.get("/{user_id}")
def get_user_detail(
    user_id: int,
    current_user: User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取用户详情"""
    current_user_id = current_user.id if current_user else None
    result = UserService.get_user_detail(db, user_id, current_user_id)
    return {"data": result}


@router.post("/{user_id}/follow")
def follow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """关注用户"""
    UserService.follow_user(db, current_user.id, user_id)
    return {"message": "关注成功"}


@router.delete("/{user_id}/follow")
def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消关注"""
    UserService.unfollow_user(db, current_user.id, user_id)
    return {"message": "已取消关注"}


@router.get("/following")
def get_following(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取关注列表"""
    result = UserService.get_following(db, current_user.id, page, page_size)
    return {"data": result}


@router.get("/followers")
def get_followers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取粉丝列表"""
    result = UserService.get_followers(db, current_user.id, page, page_size, current_user.id)
    return {"data": result}
