"""评论模块 - 单元测试"""

import pytest

from app.services.auth_service import AuthService
from app.services.post_service import PostService
from app.services.comment_service import CommentService
from app.schemas.user import UserCreate
from app.schemas.post import PostCreate
from app.schemas.comment import CommentCreate


class TestCommentService:
    """评论服务测试"""

    @pytest.fixture
    def setup_user_and_post(self, db):
        """创建测试用户和帖子"""
        user_data = UserCreate(
            username="commentuser",
            email="comment@example.com",
            password="password123"
        )
        user = AuthService.register(db, user_data)["user"]

        post_data = PostCreate(
            title="评论测试帖子标题",
            content="这是评论测试帖子的内容部分，至少需要十个字",
            category="a_stock"
        )
        post = PostService.create_post(db, user.id, post_data)

        return user, post

    def test_create_comment(self, db, setup_user_and_post):
        """测试创建评论"""
        user, post = setup_user_and_post
        data = CommentCreate(content="这是一条测试评论")

        comment = CommentService.create_comment(db, post.id, user.id, data)
        assert comment.content == data.content
        assert comment.post_id == post.id
        assert comment.user_id == user.id

    def test_get_comments(self, db, setup_user_and_post):
        """测试获取评论列表"""
        user, post = setup_user_and_post

        # 创建2条评论
        for i in range(2):
            data = CommentCreate(content=f"测试评论内容{i}")
            CommentService.create_comment(db, post.id, user.id, data)

        result = CommentService.get_comments(db, post.id)
        assert result["total"] == 2
        assert len(result["list"]) == 2

    def test_delete_comment(self, db, setup_user_and_post):
        """测试删除评论"""
        user, post = setup_user_and_post
        data = CommentCreate(content="要删除的评论")
        comment = CommentService.create_comment(db, post.id, user.id, data)

        CommentService.delete_comment(db, comment.id, user.id)

        result = CommentService.get_comments(db, post.id)
        assert result["total"] == 0

    def test_like_comment(self, db, setup_user_and_post):
        """测试点赞评论"""
        user, post = setup_user_and_post
        data = CommentCreate(content="点赞测试评论")
        comment = CommentService.create_comment(db, post.id, user.id, data)

        CommentService.like_comment(db, comment.id, user.id)

        result = CommentService.get_comments(db, post.id, current_user_id=user.id)
        assert result["list"][0]["like_count"] == 1
        assert result["list"][0]["is_liked"] == True

    def test_reply_comment(self, db, setup_user_and_post):
        """测试楼中楼回复"""
        user, post = setup_user_and_post

        # 创建父评论
        parent_data = CommentCreate(content="父评论")
        parent = CommentService.create_comment(db, post.id, user.id, parent_data)

        # 创建子评论
        reply_data = CommentCreate(content="回复父评论", parent_id=parent.id)
        reply = CommentService.create_comment(db, post.id, user.id, reply_data)

        assert reply.parent_id == parent.id
