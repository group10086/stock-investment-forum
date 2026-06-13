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
    keyword: str = Query("", min_length=0, max_length=100),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """全局搜索"""
    current_user_id = current_user.id if current_user else None
    result = SearchService.search(db, keyword, page, page_size, current_user_id)
    return {"data": result}
