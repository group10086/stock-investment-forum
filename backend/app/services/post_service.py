"""帖子服务 - 内容系统"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.models.user import User
from app.models.post import Post
from app.models.follow import Follow
from app.models.post_like import PostLike
from app.models.bookmark import Bookmark
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    """帖子服务"""

    @staticmethod
    def get_post_list(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        sort: str = "newest",
        category: str = None,
        user_id: int = None,
        current_user_id: int = None
    ) -> dict:
        """获取帖子列表"""
        from app.utils.pagination import paginate

        query = db.query(Post).filter(Post.is_deleted == False)

        # 筛选分�?
        if category:
            query = query.filter(Post.category == category)

        # 筛选用�?
        if user_id:
            query = query.filter(Post.user_id == user_id)

        # 排序
        if sort == "newest":
            query = query.order_by(Post.is_top.desc(), Post.created_at.desc())
        elif sort == "hot":
            query = query.order_by(Post.is_top.desc(), Post.like_count.desc(), Post.view_count.desc())
        elif sort == "essence":
            query = query.filter(Post.is_essence == True).order_by(Post.created_at.desc())
        elif sort == "following":
            if not current_user_id:
                return {"list": [], "total": 0, "page": page, "page_size": page_size, "has_more": False}
            # 获取关注用户的帖�?
            following_ids = db.query(Follow.followed_id).filter(
                Follow.follower_id == current_user_id
            ).subquery()
            query = query.filter(Post.user_id.in_(following_ids)).order_by(Post.created_at.desc())
        else:
            query = query.order_by(Post.created_at.desc())

        items, total, has_more = paginate(query, page, page_size)

        post_list = []
        for post in items:
            post_data = PostService._post_to_dict(post, db, current_user_id)
            post_list.append(post_data)

        return {
            "list": post_list,
            "total": total,
            "page": page,
            "page_size": page_size,
            "has_more": has_more
        }

    @staticmethod
    def get_post_detail(db: Session, post_id: int, current_user_id: int = None) -> dict:
        """获取帖子详情"""
        post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == False).first()
        if not post:
            raise HTTPException(status_code=404, detail="帖子不存�?)

        # 增加浏览�?
        post.view_count += 1
        db.commit()

        return PostService._post_to_dict(post, db, current_user_id, detail=True)

    @staticmethod
    def create_post(db: Session, user_id: int, data: PostCreate) -> Post:
        """创建帖子"""
        post = Post(
            user_id=user_id,
            title=data.title,
            content=data.content,
            summary=data.summary or data.content[:200] if len(data.content) > 200 else data.content,
            category=data.category or "other",
            tags=data.tags or [],
            images=data.images or [],
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def update_post(db: Session, post_id: int, user_id: int, data: PostUpdate) -> Post:
        """更新帖子"""
        post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == False).first()
        if not post:
            raise HTTPException(status_code=404, detail="帖子不存�?)
        if post.user_id != user_id:
            raise HTTPException(status_code=403, detail="无权修改他人帖子")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(post, key, value)

        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def delete_post(db: Session, post_id: int, user_id: int):
        """删除帖子（软删除�?""
        post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == False).first()
        if not post:
            raise HTTPException(status_code=404, detail="帖子不存�?)
        if post.user_id != user_id:
            raise HTTPException(status_code=403, detail="无权删除他人帖子")

        post.is_deleted = True
        db.commit()

    @staticmethod
    def like_post(db: Session, post_id: int, user_id: int):
        """点赞帖子"""
        post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == False).first()
        if not post:
            raise HTTPException(status_code=404, detail="帖子不存�?)

        existing = db.query(PostLike).filter(
            PostLike.user_id == user_id,
            PostLike.post_id == post_id
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="已经点赞过了")

        like = PostLike(user_id=user_id, post_id=post_id)
        db.add(like)
        post.like_count += 1
        db.commit()

    @staticmethod
    def unlike_post(db: Session, post_id: int, user_id: int):
        """取消点赞"""
        existing = db.query(PostLike).filter(
            PostLike.user_id == user_id,
            PostLike.post_id == post_id
        ).first()

        if not existing:
            raise HTTPException(status_code=400, detail="尚未点赞")

        post = db.query(Post).filter(Post.id == post_id).first()
        db.delete(existing)
        if post:
            post.like_count = max(0, post.like_count - 1)
        db.commit()

    @staticmethod
    def bookmark_post(db: Session, post_id: int, user_id: int):
        """收藏帖子"""
        post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == False).first()
        if not post:
            raise HTTPException(status_code=404, detail="帖子不存�?)

        existing = db.query(Bookmark).filter(
            Bookmark.user_id == user_id,
            Bookmark.post_id == post_id
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="已经收藏过了")

        bookmark = Bookmark(user_id=user_id, post_id=post_id)
        db.add(bookmark)
        post.bookmark_count += 1
        db.commit()

    @staticmethod
    def unbookmark_post(db: Session, post_id: int, user_id: int):
        """取消收藏"""
        existing = db.query(Bookmark).filter(
            Bookmark.user_id == user_id,
            Bookmark.post_id == post_id
        ).first()

        if not existing:
            raise HTTPException(status_code=400, detail="尚未收藏")

        post = db.query(Post).filter(Post.id == post_id).first()
        db.delete(existing)
        if post:
            post.bookmark_count = max(0, post.bookmark_count - 1)
        db.commit()

    @staticmethod
    def get_user_bookmarks(db: Session, user_id: int, page: int = 1, page_size: int = 10) -> dict:
        """获取用户收藏的帖�?""
        from app.utils.pagination import paginate

        query = db.query(Post).join(
            Bookmark, Bookmark.post_id == Post.id
        ).filter(
            Bookmark.user_id == user_id,
            Post.is_deleted == False
        ).order_by(Bookmark.created_at.desc())

        items, total, has_more = paginate(query, page, page_size)

        bookmarks = []
        for post in items:
            bookmarks.append(PostService._post_to_dict(post, db, user_id))

        return {"list": bookmarks, "total": total, "has_more": has_more}

    @staticmethod
    def _post_to_dict(post, db: Session, current_user_id: int = None, detail: bool = False) -> dict:
        """将帖子对象转为字�?""
        user = db.query(User).filter(User.id == post.user_id).first()

        is_liked = False
        is_bookmarked = False
        if current_user_id:
            is_liked = db.query(PostLike).filter(
                PostLike.user_id == current_user_id,
                PostLike.post_id == post.id
            ).first() is not None
            is_bookmarked = db.query(Bookmark).filter(
                Bookmark.user_id == current_user_id,
                Bookmark.post_id == post.id
            ).first() is not None

        result = {
            "id": post.id,
            "user_id": post.user_id,
            "title": post.title,
            "summary": post.summary,
            "category": post.category,
            "images": post.images or [],
            "tags": post.tags or [],
            "is_top": post.is_top,
            "is_essence": post.is_essence,
            "is_hot": post.is_hot,
            "view_count": post.view_count,
            "like_count": post.like_count,
            "comment_count": post.comment_count,
            "is_liked": is_liked,
            "is_bookmarked": is_bookmarked,
            "user": {
                "id": user.id if user else None,
                "nickname": user.nickname if user else "已注销",
                "avatar": user.avatar if user else "",
            },
            "created_at": post.created_at.isoformat() if post.created_at else None,
        }

        if detail:
            result["content"] = post.content
            result["bookmark_count"] = post.bookmark_count
            result["updated_at"] = post.updated_at.isoformat() if post.updated_at else None

        return result
