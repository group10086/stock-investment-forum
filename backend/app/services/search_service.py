"""搜索服务 - 信息整合系统"""

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.post import Post
from app.services.post_service import PostService


class SearchService:
    """搜索服务"""

    @staticmethod
    def search(
        db: Session,
        keyword: str = "",
        page: int = 1,
        page_size: int = 20,
        sort: str = "newest",
        category: str = None,
        date_from: str = None,
        date_to: str = None,
        current_user_id: int = None
    ) -> dict:
        """全局搜索 + 高级筛选"""
        query = db.query(Post).filter(Post.is_deleted == False)

        # 关键词搜索
        if keyword:
            search_term = f"%{keyword}%"
            query = query.filter(
                (Post.title.ilike(search_term) | Post.content.ilike(search_term))
            )

        # 分类筛选
        if category:
            query = query.filter(Post.category == category)

        # 时间筛选
        if date_from:
            query = query.filter(Post.created_at >= date_from)
        if date_to:
            query = query.filter(Post.created_at <= date_to)

        # 排序
        if sort == "newest":
            query = query.order_by(Post.created_at.desc())
        elif sort == "hot":
            query = query.order_by(Post.like_count.desc(), Post.view_count.desc())
        elif sort == "essence":
            query = query.filter(Post.is_essence == True).order_by(Post.created_at.desc())
        else:
            query = query.order_by(Post.created_at.desc())

        from app.utils.pagination import paginate
        posts, post_total, has_more = paginate(query, page, page_size)

        post_list = [PostService._post_to_dict(p, db, current_user_id) for p in posts]

        # 搜索用户
        user_list = []
        if keyword:
            user_query = db.query(User).filter(
                User.nickname.ilike(f"%{keyword}%")
            ).limit(10)
            for user in user_query.all():
                user_list.append({
                    "id": user.id,
                    "nickname": user.nickname,
                    "avatar": user.avatar,
                    "bio": user.bio,
                })

        return {
            "posts": post_list,
            "users": user_list,
            "total": post_total,
            "has_more": has_more,
        }

    @staticmethod
    def suggest(db: Session, keyword: str) -> list:
        """搜索联想：根据输入自动补全"""
        if not keyword or len(keyword) < 1:
            return []
        term = f"{keyword}%"
        posts = db.query(Post.title).filter(
            Post.is_deleted == False,
            Post.title.ilike(term)
        ).distinct().limit(5).all()
        users = db.query(User.nickname).filter(
            User.nickname.ilike(term)
        ).distinct().limit(5).all()
        return {
            "posts": [p[0] for p in posts],
            "users": [u[0] for u in users],
        }
