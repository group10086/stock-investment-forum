"""用户路由 - 用户系统"""

from fastapi import APIRouter, Depends, Query, HTTPException
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


# ========== 星标关注 ==========

from app.models.star_follow import StarFollow


@router.post("/{user_id}/star")
def star_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """星标关注用户"""
    existing = db.query(StarFollow).filter(
        StarFollow.user_id == current_user.id, StarFollow.starred_user_id == user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="已星标该用户")
    sf = StarFollow(user_id=current_user.id, starred_user_id=user_id)
    db.add(sf)
    db.commit()
    return {"message": "已星标"}


@router.delete("/{user_id}/star")
def unstar_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消星标关注"""
    sf = db.query(StarFollow).filter(
        StarFollow.user_id == current_user.id, StarFollow.starred_user_id == user_id
    ).first()
    if not sf:
        raise HTTPException(status_code=400, detail="未星标该用户")
    db.delete(sf)
    db.commit()
    return {"message": "已取消星标"}


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


# ========== 成就系统 ==========

from app.services.admin_service import AdminService


@router.get("/{user_id}/achievements")
def get_achievements(
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取用户成就"""
    result = AdminService.get_achievements(db, user_id)
    rank = AdminService.get_user_rank(db, user_id)
    return {"data": {**result, "score": rank["score"], "level": rank["level"], "title": rank["title"]}}


# ========== 积分与等级 ==========

@router.get("/{user_id}/rank")
def get_user_rank(
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取用户积分等级"""
    result = AdminService.get_user_rank(db, user_id)
    return {"data": result}
