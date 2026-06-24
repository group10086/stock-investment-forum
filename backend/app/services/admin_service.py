"""管理运营服务 - 管理运营系统"""

from datetime import datetime, timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.report import Report
from app.models.sensitive_word import SensitiveWord
from app.utils.sensitive_filter import sensitive_filter


class AdminService:
    """管理运营服务"""

    # ========== 敏感词管理 ==========

    @staticmethod
    def get_sensitive_words(db: Session) -> list:
        """获取敏感词列表"""
        words = db.query(SensitiveWord).all()
        return [
            {"id": w.id, "word": w.word, "replacement": w.replacement}
            for w in words
        ]

    @staticmethod
    def add_sensitive_word(db: Session, word: str, replacement: str = "***") -> SensitiveWord:
        """添加敏感词"""
        existing = db.query(SensitiveWord).filter(SensitiveWord.word == word).first()
        if existing:
            raise HTTPException(status_code=400, detail="敏感词已存在")

        sw = SensitiveWord(word=word, replacement=replacement)
        db.add(sw)
        db.commit()
        db.refresh(sw)

        # 重新加载敏感词过滤器
        AdminService._reload_sensitive_filter(db)

        return sw

    @staticmethod
    def delete_sensitive_word(db: Session, word_id: int):
        """删除敏感词"""
        sw = db.query(SensitiveWord).filter(SensitiveWord.id == word_id).first()
        if not sw:
            raise HTTPException(status_code=404, detail="敏感词不存在")

        db.delete(sw)
        db.commit()

        # 重新加载敏感词过滤器
        AdminService._reload_sensitive_filter(db)

    @staticmethod
    def _reload_sensitive_filter(db: Session):
        """重新加载敏感词过滤器"""
        words = db.query(SensitiveWord).all()
        word_list = [w.word for w in words]
        sensitive_filter.build(word_list)

    # ========== 举报管理 ==========

    @staticmethod
    def get_reports(db: Session, status: str = None, page: int = 1, page_size: int = 20) -> dict:
        """获取举报列表"""
        from app.utils.pagination import paginate

        query = db.query(Report).order_by(Report.created_at.desc())

        if status:
            query = query.filter(Report.status == status)

        items, total, has_more = paginate(query, page, page_size)

        report_list = []
        for report in items:
            reporter = db.query(User).filter(User.id == report.reporter_id).first()
            handler = db.query(User).filter(User.id == report.handled_by).first() if report.handled_by else None

            report_list.append({
                "id": report.id,
                "reporter_id": report.reporter_id,
                "reporter_name": reporter.nickname if reporter else "已注销",
                "target_type": report.target_type,
                "target_id": report.target_id,
                "reason": report.reason,
                "status": report.status,
                "handled_by": report.handled_by,
                "handler_name": handler.nickname if handler else None,
                "handled_at": report.handled_at.isoformat() if report.handled_at else None,
                "created_at": report.created_at.isoformat() if report.created_at else None,
            })

        return {"list": report_list, "total": total, "has_more": has_more}

    @staticmethod
    def handle_report(db: Session, report_id: int, admin_id: int, action: str):
        """处理举报"""
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            raise HTTPException(status_code=404, detail="举报不存在")

        if report.status != "pending":
            raise HTTPException(status_code=400, detail="举报已处理")

        report.status = "resolved" if action == "resolve" else "dismissed"
        report.handled_by = admin_id
        report.handled_at = datetime.now()

        # 处理被举报内容
        if action == "delete":
            if report.target_type == "post":
                post = db.query(Post).filter(Post.id == report.target_id).first()
                if post:
                    post.is_deleted = True
            elif report.target_type == "comment":
                comment = db.query(Comment).filter(Comment.id == report.target_id).first()
                if comment:
                    comment.is_deleted = True

        db.commit()

    @staticmethod
    def create_report(db: Session, reporter_id: int, target_type: str, target_id: int, reason: str) -> Report:
        """创建举报"""
        report = Report(
            reporter_id=reporter_id,
            target_type=target_type,
            target_id=target_id,
            reason=reason,
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    # ========== 用户管理 ==========

    @staticmethod
    def mute_user(db: Session, user_id: int, days: int = 7):
        """禁言用户"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        user.is_muted = True
        user.muted_until = datetime.now() + timedelta(days=days)
        db.commit()

    @staticmethod
    def unmute_user(db: Session, user_id: int):
        """解除禁言"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        user.is_muted = False
        user.muted_until = None
        db.commit()

    # ========== 内容过滤 ==========

    @staticmethod
    def filter_content(content: str) -> str:
        """过滤内容中的敏感词"""
        if not sensitive_filter._initialized:
            return content
        return sensitive_filter.filter(content)

    @staticmethod
    def check_content(content: str) -> bool:
        """检查内容是否包含敏感词"""
        if not sensitive_filter._initialized:
            return False
        return sensitive_filter.contains_sensitive(content)

    # ========== 重复内容检测 ==========

    @staticmethod
    def detect_duplicate(db: Session, content: str, threshold: float = 0.6) -> list:
        """检测相似内容（基于简单文本相似度）"""
        if len(content) < 20:
            return []
        # 取前50字做精确匹配
        prefix = content[:50]
        recent = db.query(Post).filter(
            Post.is_deleted == False,
            Post.content.ilike(f"{prefix}%")
        ).limit(5).all()
        return [{"id": p.id, "title": p.title, "created_at": p.created_at.isoformat()} for p in recent]

    # ========== 积分与等级系统 ==========

    @staticmethod
    def add_score(db: Session, user_id: int, points: int, reason: str = "") -> dict:
        """增加用户积分"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"score": 0, "level": 0}

        current_score = getattr(user, 'score', 0) or 0
        current_score += points
        user.score = current_score

        # 计算等级：每100分升1级，最高50级
        level = min(current_score // 100, 50)
        user.level = level

        db.commit()
        return {"score": current_score, "level": level}

    @staticmethod
    def get_user_rank(db: Session, user_id: int) -> dict:
        """获取用户积分与等级"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"score": 0, "level": 0, "title": "新手上路"}
        score = getattr(user, 'score', 0) or 0
        level = getattr(user, 'level', 0) or 0
        titles = {0: "新手上路", 5: "财经达人", 10: "投资高手", 20: "股海老手", 30: "传奇投资者", 50: "论坛至尊"}
        title = "新手上路"
        for lv, t in sorted(titles.items(), reverse=True):
            if level >= lv:
                title = t
                break
        return {"score": score, "level": level, "title": title}

    # ========== 数据分析（管理员） ==========

    @staticmethod
    def get_analytics(db: Session) -> dict:
        """获取论坛统计数据"""
        from sqlalchemy import func
        total_users = db.query(User).count()
        total_posts = db.query(Post).filter(Post.is_deleted == False).count()
        total_comments = db.query(Comment).filter(Comment.is_deleted == False).count()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_posts = db.query(Post).filter(
            Post.is_deleted == False, Post.created_at >= today
        ).count()
        today_comments = db.query(Comment).filter(
            Comment.is_deleted == False, Comment.created_at >= today
        ).count()
        today_active = db.query(User.id).filter(
            User.id.in_(
                db.query(Post.user_id).filter(Post.created_at >= today).distinct().union(
                    db.query(Comment.user_id).filter(Comment.created_at >= today).distinct()
                )
            )
        ).count()

        return {
            "total_users": total_users,
            "total_posts": total_posts,
            "total_comments": total_comments,
            "today_posts": today_posts,
            "today_comments": today_comments,
            "today_active_users": today_active,
            "dau": today_active,
        }

    # ========== 成就系统 ==========

    @staticmethod
    def get_achievements(db: Session, user_id: int) -> dict:
        """获取用户成就"""
        post_count = db.query(Post).filter(Post.user_id == user_id, Post.is_deleted == False).count()
        comment_count = db.query(Comment).filter(Comment.user_id == user_id, Comment.is_deleted == False).count()
        from app.models.post_like import PostLike
        like_received = db.query(PostLike).join(Post).filter(Post.user_id == user_id).count()

        achievements = []
        if post_count >= 1:
            achievements.append({"name": "初来乍到", "desc": "发布第一篇帖子", "icon": "📝"})
        if post_count >= 10:
            achievements.append({"name": "笔耕不辍", "desc": "发布10篇帖子", "icon": "✍️"})
        if post_count >= 50:
            achievements.append({"name": "高产作者", "desc": "发布50篇帖子", "icon": "🏆"})
        if comment_count >= 10:
            achievements.append({"name": "热心评论", "desc": "发表10条评论", "icon": "💬"})
        if comment_count >= 100:
            achievements.append({"name": "评论达人", "desc": "发表100条评论", "icon": "🎯"})
        if like_received >= 10:
            achievements.append({"name": "人气之星", "desc": "获得10个赞", "icon": "⭐"})

        return {"post_count": post_count, "comment_count": comment_count, "like_received": like_received, "achievements": achievements}
