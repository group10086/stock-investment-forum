"""认证路由 - 用户系统"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register")
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    result = AuthService.register(db, user_data)
    return {
        "message": "注册成功",
        "data": {
            "user": UserResponse.model_validate(result["user"]),
            "token": result["token"],
        }
    }


@router.post("/login")
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    result = AuthService.login(db, login_data)
    return {
        "message": "登录成功",
        "data": {
            "user": UserResponse.model_validate(result["user"]),
            "token": result["token"],
        }
    }
