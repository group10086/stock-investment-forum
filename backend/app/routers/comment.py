"""评论路由 - 内容系统"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import CommentService
from app.services.admin_service import AdminService
from app.utils.jwt_handler import get_current_user, get_optional_user

router = APIRouter(prefix="/api", tags=["评论"])


@router.get("/posts/{post_id}/comments")
def get_comments(
    post_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取评论列表"""
    current_user_id = current_user.id if current_user else None
    result = CommentService.get_comments(db, post_id, page, page_size, current_user_id)
    return {"data": result}


@router.post("/posts/{post_id}/comments")
def create_comment(
    post_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建评论"""
    # 检查是否被禁言
    if current_user.is_muted:
        return {"message": "您已被禁言，无法发表评论"}, 403

    # 敏感词过滤
    filtered_content = AdminService.filter_content(data.content)

    comment = CommentService.create_comment(
        db, post_id, current_user.id,
        CommentCreate(content=filtered_content, parent_id=data.parent_id)
    )
    return {"message": "评论成功", "data": CommentResponse.model_validate(comment)}


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除评论"""
    CommentService.delete_comment(db, comment_id, current_user.id)
    return {"message": "删除成功"}


@router.post("/comments/{comment_id}/like")
def like_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """点赞评论"""
    CommentService.like_comment(db, comment_id, current_user.id)
    return {"message": "点赞成功"}
