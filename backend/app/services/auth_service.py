"""认证服务 - 用户系统"""

from fastapi import HTTPException, status
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.jwt_handler import create_access_token


def _hash_password(password: str) -> str:
    """安全地哈希密码，截断到72字节（bcrypt限制）"""
    return bcrypt.hash(password[:72])


class AuthService:
    """用户认证服务"""

    @staticmethod
    def register(db: Session, user_data: UserCreate) -> dict:
        """用户注册"""
        # 检查用户名是否已存在
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已被使用"
            )

        # 检查邮箱是否已存在
        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )

        # 创建用户
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=_hash_password(user_data.password),
            nickname=user_data.username,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # 注册奖励积分
        from app.services.admin_service import AdminService
        AdminService.add_score(db, user.id, 10, "注册奖励")

        # 生成token
        token = create_access_token({"user_id": user.id})

        return {
            "user": user,
            "token": token
        }

    @staticmethod
    def login(db: Session, login_data: UserLogin) -> dict:
        """用户登录"""
        # 支持邮箱或用户名登录
        user = db.query(User).filter(
            (User.email == login_data.email) | (User.username == login_data.email)
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号或密码错误"
            )

        if not bcrypt.verify(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号或密码错误"
            )

        # 检查是否被禁言/封号
        if user.is_muted and user.muted_until:
            from datetime import datetime
            if user.muted_until > datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"账号已被禁言至{user.muted_until.strftime('%Y-%m-%d %H:%M')}"
                )
            else:
                user.is_muted = False
                user.muted_until = None
                db.commit()

        # 生成token
        token = create_access_token({"user_id": user.id})

        return {
            "user": user,
            "token": token
        }