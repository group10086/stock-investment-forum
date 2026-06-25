"""搜索路由 - 信息整合系统"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.search_service import SearchService
from app.utils.jwt_handler import get_optional_user

router = APIRouter(prefix="/api/search", tags=["搜索"])


@router.get("")
def search(
    keyword: str = Query("", max_length=100),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    sort: str = Query("newest", pattern="^(newest|hot|essence)$"),
    category: str = Query(None),
    date_from: str = Query(None),
    date_to: str = Query(None),
    current_user: User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """全局搜索 + 高级筛选"""
    current_user_id = current_user.id if current_user else None
    result = SearchService.search(
        db, keyword, page, page_size, sort, category, date_from, date_to, current_user_id
    )
    return {"data": result}


@router.get("/suggest")
def suggest(
    keyword: str = Query("", max_length=50),
    db: Session = Depends(get_db)
):
    """搜索联想"""
    if not keyword:
        return {"data": {"posts": [], "users": []}}
    return {"data": result}
