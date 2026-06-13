"""管理运营路由 - 管理运营系统"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.admin_service import AdminService
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/api/admin", tags=["管理运营"])


def require_admin(current_user: User = Depends(get_current_user)):
    """管理员权限验证"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, message="需要管理员权限")
    return current_user


# ========== 举报管理 ==========

@router.get("/reports")
def get_reports(
    status: str = Query(None, pattern="^(pending|resolved|dismissed)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取举报列表（管理员）"""
    result = AdminService.get_reports(db, status, page, page_size)
    return {"data": result}


@router.put("/reports/{report_id}")
def handle_report(
    report_id: int,
    action: str = Query(..., pattern="^(resolve|dismiss|delete)$"),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """处理举报（管理员）"""
    AdminService.handle_report(db, report_id, admin.id, action)
    return {"message": "处理成功"}


# ========== 用户管理 ==========

@router.post("/user/{user_id}/mute")
def mute_user(
    user_id: int,
    days: int = Query(7, ge=1, le=365),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """禁言用户（管理员）"""
    AdminService.mute_user(db, user_id, days)
    return {"message": f"已禁言用户{user_id}，持续{days}天"}


@router.post("/user/{user_id}/unmute")
def unmute_user(
    user_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """解除禁言（管理员）"""
    AdminService.unmute_user(db, user_id)
    return {"message": "已解除禁言"}


# ========== 敏感词管理 ==========

@router.get("/sensitive-words")
def get_sensitive_words(
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取敏感词列表（管理员）"""
    words = AdminService.get_sensitive_words(db)
    return {"data": words}


@router.post("/sensitive-words")
def add_sensitive_word(
    word: str,
    replacement: str = "***",
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """添加敏感词（管理员）"""
    sw = AdminService.add_sensitive_word(db, word, replacement)
    return {"message": "添加成功", "data": {"id": sw.id, "word": sw.word}}


@router.delete("/sensitive-words/{word_id}")
def delete_sensitive_word(
    word_id: int,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """删除敏感词（管理员）"""
    AdminService.delete_sensitive_word(db, word_id)
    return {"message": "删除成功"}
