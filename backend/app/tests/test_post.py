"""帖子服务 - 单元测试"""

import pytest
from fastapi import HTTPException

from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostUpdate


class TestPostService:
    """帖子服务测试"""

    def test_create_post_success(self, db, test_user):
        """测试创建帖子成功"""
        data = PostCreate(
            title="我的第一个帖子",
            content="这是帖子的详细内容，包含足够的信息。",
            category="tech",
            tags=["python", "fastapi"]
        )
        post = PostService.create_post(db, test_user.id, data)

        assert post.id is not None
        assert post.title == "我的第一个帖子"
        assert post.content == "这是帖子的详细内容，包含足够的信息。"
        assert post.user_id == test_user.id
        assert post.category == "tech"
        assert post.tags == ["python", "fastapi"]

    def test_create_post_minimal(self, db, test_user):
        """测试最小字段创建帖子"""
        data = PostCreate(
            title="最短标题",
            content="这是最短的内容，但必须超过10个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        assert post.id is not None
        assert post.title == "最短标题"
        assert post.summary is not None

    def test_get_post_detail_success(self, db, test_user):
        """测试获取帖子详情成功"""
        # 先创建帖子
        data = PostCreate(
            title="详情测试帖子",
            content="这是用来测试详情的帖子内容。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 获取详情
        result = PostService.get_post_detail(db, post.id, test_user.id)

        assert result["id"] == post.id
        assert result["title"] == "详情测试帖子"
        assert result["content"] == "这是用来测试详情的帖子内容。"
        assert result["user"]["id"] == test_user.id
        assert "is_liked" in result
        assert "is_bookmarked" in result

    def test_get_post_detail_not_found(self, db):
        """测试获取不存在的帖子"""
        with pytest.raises(HTTPException) as exc:
            PostService.get_post_detail(db, 99999)
        assert exc.value.status_code == 404
        assert "不存在" in str(exc.value.detail)

    def test_get_post_list_success(self, db, test_user):
        """测试获取帖子列表成功"""
        # 创建多个帖子
        for i in range(3):
            data = PostCreate(
                title=f"帖子{i}",
                content=f"这是第{i}个帖子的内容。"
            )
            PostService.create_post(db, test_user.id, data)

        result = PostService.get_post_list(db, page=1, page_size=10)

        assert result["total"] >= 3
        assert result["page"] == 1
        assert result["page_size"] == 10
        assert len(result["list"]) >= 3
        assert "has_more" in result

    def test_get_post_list_with_category_filter(self, db, test_user):
        """测试按分类筛选帖子"""
        # 创建不同分类的帖子
        data1 = PostCreate(
            title="技术帖",
            content="这是技术内容。",
            category="tech"
        )
        PostService.create_post(db, test_user.id, data1)

        data2 = PostCreate(
            title="娱乐帖",
            content="这是娱乐内容。",
            category="fun"
        )
        PostService.create_post(db, test_user.id, data2)

        result = PostService.get_post_list(db, category="tech")

        assert len(result["list"]) >= 1
        for post in result["list"]:
            assert post["category"] == "tech"

    def test_get_post_list_with_user_filter(self, db, test_user):
        """测试按用户筛选帖子"""
        data = PostCreate(
            title="用户筛选测试",
            content="这是测试内容。"
        )
        PostService.create_post(db, test_user.id, data)

        result = PostService.get_post_list(db, user_id=test_user.id)

        assert len(result["list"]) >= 1
        for post in result["list"]:
            assert post["user_id"] == test_user.id

    def test_get_post_list_sort_newest(self, db, test_user):
        """测试最新排序"""
        # 创建两个帖子，时间有先后
        import time
        data1 = PostCreate(
            title="第一个帖子",
            content="这是第一个帖子的内容。"
        )
        PostService.create_post(db, test_user.id, data1)
        time.sleep(0.1)

        data2 = PostCreate(
            title="第二个帖子",
            content="这是第二个帖子的内容。"
        )
        PostService.create_post(db, test_user.id, data2)

        result = PostService.get_post_list(db, sort="newest")

        # 最新的应该排在前面
        assert len(result["list"]) >= 2
        assert result["list"][0]["title"] == "第二个帖子"

    def test_update_post_success(self, db, test_user):
        """测试更新帖子成功"""
        # 创建帖子
        data = PostCreate(
            title="原标题",
            content="原始内容。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 更新帖子
        update_data = PostUpdate(
            title="新标题",
            content="更新后的内容。"
        )
        updated = PostService.update_post(db, post.id, test_user.id, update_data)

        assert updated.title == "新标题"
        assert updated.content == "更新后的内容。"

    def test_update_post_unauthorized(self, db, test_user):
        """测试无权更新他人帖子"""
        # 创建第一个用户的帖子
        data = PostCreate(
            title="他人帖子",
            content="这是他人创建的帖子。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 创建第二个用户（模拟另一个用户）
        from app.services.auth_service import AuthService
        from app.schemas.user import UserCreate
        user2_data = UserCreate(
            username="user2",
            email="user2@example.com",
            password="password123"
        )
        user2 = AuthService.register(db, user2_data)["user"]

        # 用第二个用户尝试更新第一个用户的帖子
        update_data = PostUpdate(title="恶意修改")
        with pytest.raises(HTTPException) as exc:
            PostService.update_post(db, post.id, user2.id, update_data)
        assert exc.value.status_code == 403

    def test_delete_post_success(self, db, test_user):
        """测试删除帖子成功"""
        data = PostCreate(
            title="待删除帖子",
            content="这个帖子将被删除。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 删除帖子
        PostService.delete_post(db, post.id, test_user.id)

        # 验证帖子已被软删除
        from app.models.post import Post
        deleted_post = db.query(Post).filter(Post.id == post.id).first()
        assert deleted_post.is_deleted is True

    def test_delete_post_unauthorized(self, db, test_user):
        """测试无权删除他人帖子"""
        data = PostCreate(
            title="他人帖子",
            content="这是他人的帖子。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 模拟另一个用户尝试删除
        from app.services.auth_service import AuthService
        from app.schemas.user import UserCreate
        user2_data = UserCreate(
            username="user3",
            email="user3@example.com",
            password="password123"
        )
        user2 = AuthService.register(db, user2_data)["user"]

        with pytest.raises(HTTPException) as exc:
            PostService.delete_post(db, post.id, user2.id)
        assert exc.value.status_code == 403

    def test_like_post_success(self, db, test_user):
        """测试点赞帖子成功"""
        data = PostCreate(
            title="点赞测试",
            content="这个帖子将被点赞。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 点赞
        PostService.like_post(db, post.id, test_user.id)

        # 验证点赞数增加
        from app.models.post import Post
        updated_post = db.query(Post).filter(Post.id == post.id).first()
        assert updated_post.like_count == 1

    def test_like_post_already_liked(self, db, test_user):
        """测试重复点赞"""
        data = PostCreate(
            title="重复点赞测试",
            content="这个帖子将被重复点赞。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 第一次点赞
        PostService.like_post(db, post.id, test_user.id)

        # 第二次点赞（应该报错）
        with pytest.raises(HTTPException) as exc:
            PostService.like_post(db, post.id, test_user.id)
        assert exc.value.status_code == 400

    def test_unlike_post_success(self, db, test_user):
        """测试取消点赞成功"""
        data = PostCreate(
            title="取消点赞测试",
            content="这个帖子将被点赞然后取消。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 点赞
        PostService.like_post(db, post.id, test_user.id)
        # 取消点赞
        PostService.unlike_post(db, post.id, test_user.id)

        from app.models.post import Post
        updated_post = db.query(Post).filter(Post.id == post.id).first()
        assert updated_post.like_count == 0

    def test_bookmark_post_success(self, db, test_user):
        """测试收藏帖子成功"""
        data = PostCreate(
            title="收藏测试",
            content="这个帖子将被收藏。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 收藏
        PostService.bookmark_post(db, post.id, test_user.id)

        from app.models.post import Post
        updated_post = db.query(Post).filter(Post.id == post.id).first()
        assert updated_post.bookmark_count == 1

    def test_bookmark_post_already_bookmarked(self, db, test_user):
        """测试重复收藏"""
        data = PostCreate(
            title="重复收藏测试",
            content="这个帖子将被重复收藏。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 第一次收藏
        PostService.bookmark_post(db, post.id, test_user.id)

        # 第二次收藏（应该报错）
        with pytest.raises(HTTPException) as exc:
            PostService.bookmark_post(db, post.id, test_user.id)
        assert exc.value.status_code == 400

    def test_unbookmark_post_success(self, db, test_user):
        """测试取消收藏成功"""
        data = PostCreate(
            title="取消收藏测试",
            content="这个帖子将被收藏然后取消。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 收藏
        PostService.bookmark_post(db, post.id, test_user.id)
        # 取消收藏
        PostService.unbookmark_post(db, post.id, test_user.id)

        from app.models.post import Post
        updated_post = db.query(Post).filter(Post.id == post.id).first()
        assert updated_post.bookmark_count == 0

    def test_get_user_bookmarks_success(self, db, test_user):
        """测试获取用户收藏列表"""
        # 创建多个帖子并收藏
        for i in range(3):
            data = PostCreate(
                title=f"收藏帖子{i}",
                content=f"这是第{i}个被收藏的帖子。"
            )
            post = PostService.create_post(db, test_user.id, data)
            PostService.bookmark_post(db, post.id, test_user.id)

        result = PostService.get_user_bookmarks(db, test_user.id)

        assert result["total"] >= 3
        assert len(result["list"]) >= 3

    def test_get_post_list_with_following_sort(self, db, test_user):
        """测试关注排序（没有关注时返回空列表）"""
        result = PostService.get_post_list(db, sort="following", current_user_id=test_user.id)

        # 没有关注时，应该返回空列表
        assert result["list"] == []
        assert result["total"] == 0

    def test_get_post_list_following_without_user(self, db):
        """测试关注排序但未登录"""
        result = PostService.get_post_list(db, sort="following", current_user_id=None)

        assert result["list"] == []
        assert result["total"] == 0
        assert result["has_more"] is False