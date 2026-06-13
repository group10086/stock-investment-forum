"""帖子模块 - 单元测试"""

import pytest
from fastapi import status

from app.models.user import User
from app.models.post import Post
from app.services.auth_service import AuthService
from app.services.post_service import PostService
from app.schemas.user import UserCreate
from app.schemas.post import PostCreate


class TestPostService:
    """帖子服务测试"""

    @pytest.fixture
    def setup_user(self, db):
        """创建测试用户"""
        data = UserCreate(
            username="postuser",
            email="post@example.com",
            password="password123"
        )
        result = AuthService.register(db, data)
        return result["user"]

    def test_create_post(self, db, setup_user):
        """测试创建帖子"""
        data = PostCreate(
            title="这是一篇测试帖子的标题",
            content="这是测试帖子的内容，需要至少十个字才能发布",
            category="a_stock",
            tags=["A股", "测试"]
        )
        post = PostService.create_post(db, setup_user.id, data)

        assert post.title == data.title
        assert post.content == data.content
        assert post.category == "a_stock"
        assert post.user_id == setup_user.id

    def test_get_post_list(self, db, setup_user):
        """测试获取帖子列表"""
        # 创建2个帖子
        for i in range(2):
            data = PostCreate(
                title=f"测试帖子标题{i}",
                content=f"这是测试帖子内容{i}，需要至少十个字才能发布",
                category="a_stock"
            )
            PostService.create_post(db, setup_user.id, data)

        result = PostService.get_post_list(db, page=1, page_size=10)
        assert result["total"] == 2
        assert len(result["list"]) == 2

    def test_get_post_detail(self, db, setup_user):
        """测试获取帖子详情"""
        data = PostCreate(
            title="详情测试帖标题",
            content="这是详情测试帖的内容部分，需要至少十个字",
            category="hk_stock"
        )
        post = PostService.create_post(db, setup_user.id, data)

        detail = PostService.get_post_detail(db, post.id)
        assert detail["title"] == data.title
        assert detail["content"] == data.content
        assert detail["view_count"] >= 1  # 访问后浏览量增加

    def test_delete_post(self, db, setup_user):
        """测试删除帖子"""
        data = PostCreate(
            title="要删除的帖子标题",
            content="这是要删除的帖子内容，需要至少十个字",
            category="us_stock"
        )
        post = PostService.create_post(db, setup_user.id, data)

        PostService.delete_post(db, post.id, setup_user.id)

        # 软删除，不应出现在列表中
        result = PostService.get_post_list(db)
        assert result["total"] == 0

    def test_like_post(self, db, setup_user):
        """测试点赞帖子"""
        data = PostCreate(
            title="点赞测试帖",
            content="这是点赞测试帖的内容，需要至少十个字",
            category="fund"
        )
        post = PostService.create_post(db, setup_user.id, data)

        PostService.like_post(db, post.id, setup_user.id)
        detail = PostService.get_post_detail(db, post.id)
        assert detail["like_count"] == 1

    def test_bookmark_post(self, db, setup_user):
        """测试收藏帖子"""
        data = PostCreate(
            title="收藏测试帖",
            content="这是收藏测试帖的内容，需要至少十个字",
            category="technical"
        )
        post = PostService.create_post(db, setup_user.id, data)

        PostService.bookmark_post(db, post.id, setup_user.id)
        bookmarks = PostService.get_user_bookmarks(db, setup_user.id)
        assert bookmarks["total"] == 1


class TestPostAPI:
    """帖子API测试"""

    @pytest.fixture
    def auth_headers(self, client, test_user_data):
        """获取认证头"""
        client.post("/api/auth/register", json=test_user_data)
        login_resp = client.post("/api/auth/login", json={
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        })
        token = login_resp.json()["data"]["token"]
        return {"Authorization": f"Bearer {token}"}

    def test_create_post_api(self, client, auth_headers):
        """测试创建帖子API"""
        post_data = {
            "title": "API测试帖子的标题部分",
            "content": "API测试帖子的内容部分，需要至少十个字才能发布成功",
            "category": "a_stock"
        }
        response = client.post("/api/posts", json=post_data, headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "发布成功"

    def test_get_posts_api(self, client):
        """测试获取帖子列表API"""
        response = client.get("/api/posts")
        assert response.status_code == status.HTTP_200_OK
