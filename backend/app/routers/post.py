"""帖子路由 - 内容系统"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.services.post_service import PostService
from app.services.admin_service import AdminService
from app.utils.jwt_handler import get_current_user, get_optional_user

router = APIRouter(prefix="/api/posts", tags=["帖子"])


@router.get("")
def get_post_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    sort: str = Query("newest", pattern="^(newest|hot|essence|following)$"),
    category: str = Query(None),
    user_id: int = Query(None),
    mine: int = Query(None),
    bookmarked: int = Query(None),
    current_user: User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取帖子列表"""
    current_user_id = current_user.id if current_user else None
    result = PostService.get_post_list(
        db, page, page_size, sort, category, user_id, current_user_id,
        mine=mine, bookmarked=bookmarked
    )
    return {"data": result}


@router.get("/{post_id}")
def get_post_detail(
    post_id: int,
    current_user: User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取帖子详情"""
    current_user_id = current_user.id if current_user else None
    result = PostService.get_post_detail(db, post_id, current_user_id)
    return {"data": result}


@router.post("")
def create_post(
    data: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建帖子"""
    # 检查是否被禁言
    if current_user.is_muted:
        return {"message": "您已被禁言，无法发布帖子"}, 403

    # 敏感词过滤
    filtered_content = AdminService.filter_content(data.content)
    filtered_title = AdminService.filter_content(data.title)

    post = PostService.create_post(
        db, current_user.id,
        PostCreate(
            title=filtered_title,
            content=filtered_content,
            summary=data.summary,
            category=data.category,
            tags=data.tags,
            images=data.images,
        )
    )
    return {"message": "发布成功", "data": PostResponse.model_validate(post)}


@router.put("/{post_id}")
def update_post(
    post_id: int,
    data: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新帖子"""
    post = PostService.update_post(db, post_id, current_user.id, data)
    return {"message": "更新成功", "data": PostResponse.model_validate(post)}


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除帖子"""
    PostService.delete_post(db, post_id, current_user.id)
    return {"message": "删除成功"}


@router.post("/{post_id}/like")
def like_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """点赞帖子"""
    PostService.like_post(db, post_id, current_user.id)
    return {"message": "点赞成功"}


@router.delete("/{post_id}/like")
def unlike_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消点赞"""
    PostService.unlike_post(db, post_id, current_user.id)
    return {"message": "已取消点赞"}


@router.post("/{post_id}/bookmark")
def bookmark_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """收藏帖子"""
    PostService.bookmark_post(db, post_id, current_user.id)
    return {"message": "收藏成功"}


@router.delete("/{post_id}/bookmark")
def unbookmark_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消收藏"""
    PostService.unbookmark_post(db, post_id, current_user.id)
    return {"message": "已取消收藏"}
