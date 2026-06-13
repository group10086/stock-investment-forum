"""评论服务 - 内容系统"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.comment_like import CommentLike
from app.schemas.comment import CommentCreate


class CommentService:
    """评论服务"""

    @staticmethod
    def get_comments(db: Session, post_id: int, page: int = 1, page_size: int = 20, current_user_id: int = None) -> dict:
        """获取评论列表"""
        from app.utils.pagination import paginate

        # 验证帖子存在
        post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == False).first()
        if not post:
            raise HTTPException(status_code=404, detail="帖子不存在")

        # 获取顶级评论
        query = db.query(Comment).filter(
            Comment.post_id == post_id,
            Comment.parent_id.is_(None),
            Comment.is_deleted == False
        ).order_by(Comment.created_at.asc())

        items, total, has_more = paginate(query, page, page_size)

        comment_list = []
        for comment in items:
            comment_data = CommentService._comment_to_dict(comment, db, current_user_id)
            # 获取子评论（楼中楼）
            replies = db.query(Comment).filter(
                Comment.parent_id == comment.id,
                Comment.is_deleted == False
            ).order_by(Comment.created_at.asc()).all()

            comment_data["replies"] = [
                CommentService._comment_to_dict(reply, db, current_user_id)
                for reply in replies
            ]

            comment_list.append(comment_data)

        return {"list": comment_list, "total": total}

    @staticmethod
    def create_comment(db: Session, post_id: int, user_id: int, data: CommentCreate) -> Comment:
        """创建评论"""
        # 验证帖子存在
        post = db.query(Post).filter(Post.id == post_id, Post.is_deleted == False).first()
        if not post:
            raise HTTPException(status_code=404, detail="帖子不存在")

        # 如果是楼中楼回复，验证父评论存在
        if data.parent_id:
            parent = db.query(Comment).filter(
                Comment.id == data.parent_id,
                Comment.post_id == post_id
            ).first()
            if not parent:
                raise HTTPException(status_code=404, detail="父评论不存在")

        comment = Comment(
            post_id=post_id,
            user_id=user_id,
            parent_id=data.parent_id,
            content=data.content,
        )
        db.add(comment)
        post.comment_count += 1
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def delete_comment(db: Session, comment_id: int, user_id: int):
        """删除评论（软删除）"""
        comment = db.query(Comment).filter(
            Comment.id == comment_id,
            Comment.is_deleted == False
        ).first()

        if not comment:
            raise HTTPException(status_code=404, detail="评论不存在")
        if comment.user_id != user_id:
            raise HTTPException(status_code=403, detail="无权删除他人评论")

        comment.is_deleted = True

        # 更新帖子评论数?
        post = db.query(Post).filter(Post.id == comment.post_id).first()
        if post:
            post.comment_count = max(0, post.comment_count - 1)

        db.commit()

    @staticmethod
    def like_comment(db: Session, comment_id: int, user_id: int):
        """点赞评论"""
        comment = db.query(Comment).filter(
            Comment.id == comment_id,
            Comment.is_deleted == False
        ).first()

        if not comment:
            raise HTTPException(status_code=404, detail="评论不存在")

        existing = db.query(CommentLike).filter(
            CommentLike.user_id == user_id,
            CommentLike.comment_id == comment_id
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="已经点赞过了")

        like = CommentLike(user_id=user_id, comment_id=comment_id)
        db.add(like)
        comment.like_count += 1
        db.commit()

    @staticmethod
    def _comment_to_dict(comment, db: Session, current_user_id: int = None) -> dict:
        """将评论对象转为字典"""
        user = db.query(User).filter(User.id == comment.user_id).first()

        is_liked = False
        if current_user_id:
            is_liked = db.query(CommentLike).filter(
                CommentLike.user_id == current_user_id,
                CommentLike.comment_id == comment.id
            ).first() is not None

        return {
            "id": comment.id,
            "post_id": comment.post_id,
            "user_id": comment.user_id,
            "parent_id": comment.parent_id,
            "content": comment.content if not comment.is_deleted else "该评论已被删除",
            "like_count": comment.like_count,
            "is_liked": is_liked,
            "is_deleted": comment.is_deleted,
            "user": {
                "id": user.id if user else None,
                "nickname": user.nickname if user else "已注销",
                "avatar": user.avatar if user else "",
            },
            "created_at": comment.created_at.isoformat() if comment.created_at else None,
        }
