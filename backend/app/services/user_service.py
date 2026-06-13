"""用户服务 - 用户系统"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.follow import Follow
from app.models.post import Post
from app.models.bookmark import Bookmark
from app.schemas.user import UserUpdate


class UserService:
    """用户信息服务"""

    @staticmethod
    def get_user_info(db: Session, user_id: int) -> User:
        """获取当前用户信息"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return user

    @staticmethod
    def update_user_info(db: Session, user_id: int, data: UserUpdate) -> User:
        """更新用户信息"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_detail(db: Session, user_id: int, current_user_id: int = None) -> dict:
        """获取用户详情页信息"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        # 统计数据
        post_count = db.query(Post).filter(
            Post.user_id == user_id, Post.is_deleted == False
        ).count()
        following_count = db.query(Follow).filter(
            Follow.follower_id == user_id
        ).count()
        follower_count = db.query(Follow).filter(
            Follow.followed_id == user_id
        ).count()

        # 是否已关注
        is_following = False
        if current_user_id and current_user_id != user_id:
            is_following = db.query(Follow).filter(
                Follow.follower_id == current_user_id,
                Follow.followed_id == user_id
            ).first() is not None

        result = {
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "bio": user.bio,
            "investment_preference": user.investment_preference,
            "github": user.github,
            "is_verified": user.is_verified,
            "is_following": is_following,
            "post_count": post_count,
            "following_count": following_count,
            "follower_count": follower_count,
            "created_at": user.created_at,
        }

        return result

    @staticmethod
    def follow_user(db: Session, follower_id: int, followed_id: int):
        """关注用户"""
        if follower_id == followed_id:
            raise HTTPException(status_code=400, detail="不能关注自己")

        user = db.query(User).filter(User.id == followed_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        existing = db.query(Follow).filter(
            Follow.follower_id == follower_id,
            Follow.followed_id == followed_id
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="已经关注了该用户")

        follow = Follow(follower_id=follower_id, followed_id=followed_id)
        db.add(follow)
        db.commit()

    @staticmethod
    def unfollow_user(db: Session, follower_id: int, followed_id: int):
        """取消关注"""
        follow = db.query(Follow).filter(
            Follow.follower_id == follower_id,
            Follow.followed_id == followed_id
        ).first()

        if not follow:
            raise HTTPException(status_code=400, detail="尚未关注该用户")

        db.delete(follow)
        db.commit()

    @staticmethod
    def get_following(db: Session, user_id: int, page: int = 1, page_size: int = 20) -> dict:
        """获取关注列表"""
        from app.utils.pagination import paginate

        query = db.query(Follow, User).join(
            User, Follow.followed_id == User.id
        ).filter(
            Follow.follower_id == user_id
        ).order_by(Follow.created_at.desc())

        items, total, has_more = paginate(query, page, page_size)

        following_list = []
        for follow, user in items:
            following_list.append({
                "id": user.id,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "bio": user.bio,
                "is_following": True,
            })

        return {"list": following_list, "total": total, "has_more": has_more}

    @staticmethod
    def get_followers(db: Session, user_id: int, page: int = 1, page_size: int = 20, current_user_id: int = None) -> dict:
        """获取粉丝列表"""
        from app.utils.pagination import paginate

        query = db.query(Follow, User).join(
            User, Follow.follower_id == User.id
        ).filter(
            Follow.followed_id == user_id
        ).order_by(Follow.created_at.desc())

        items, total, has_more = paginate(query, page, page_size)

        followers_list = []
        for follow, user in items:
            # 检查是否已互关
            is_following = False
            if current_user_id:
                is_following = db.query(Follow).filter(
                    Follow.follower_id == current_user_id,
                    Follow.followed_id == user.id
                ).first() is not None

            followers_list.append({
                "id": user.id,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "bio": user.bio,
                "is_following": is_following,
            })

        return {"list": followers_list, "total": total, "has_more": has_more}
