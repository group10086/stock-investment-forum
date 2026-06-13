"""搜索服务 - 信息整合系统"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.post import Post
from app.services.post_service import PostService


class SearchService:
    """搜索服务"""

    @staticmethod
    def search(db: Session, keyword: str, page: int = 1, page_size: int = 20, current_user_id: int = None) -> dict:
        """全局搜索"""
        if not keyword:
            return {"posts": [], "users": [], "total": 0}

        search_term = f"%{keyword}%"

        # 搜索帖子
        post_query = db.query(Post).filter(
            Post.is_deleted == False,
            (Post.title.ilike(search_term) | Post.content.ilike(search_term))
        ).order_by(Post.created_at.desc())

        from app.utils.pagination import paginate
        posts, post_total, _ = paginate(post_query, page, page_size)

        post_list = []
        for post in posts:
            post_list.append(PostService._post_to_dict(post, db, current_user_id))

        # 搜索用户
        user_query = db.query(User).filter(
            User.nickname.ilike(search_term)
        ).limit(10)

        users = user_query.all()
        user_list = [
            {
                "id": user.id,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "bio": user.bio,
            }
            for user in users
        ]

        return {
            "posts": post_list,
            "users": user_list,
            "total": post_total,
        }
