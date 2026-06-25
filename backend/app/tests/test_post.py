"""帖子服务 - 单元测试"""

import pytest
from fastapi import HTTPException

from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostUpdate
from app.models.user import User


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
            title="最短标题测试",
            content="这是最短的内容，但必须超过10个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        assert post.id is not None
        assert post.title == "最短标题测试"
        assert post.summary is not None

    def test_get_post_detail_success(self, db, test_user):
        """测试获取帖子详情成功"""
        data = PostCreate(
            title="详情测试帖子",
            content="这是用来测试详情的帖子内容。"
        )
        post = PostService.create_post(db, test_user.id, data)

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
        for i in range(3):
            data = PostCreate(
                title=f"测试帖子{i}号",
                content=f"这是第{i}个帖子的内容，足够长了。"
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
        data1 = PostCreate(
            title="技术帖测试",
            content="这是技术内容，超过十个字符了。",
            category="other"
        )
        PostService.create_post(db, test_user.id, data1)

        data2 = PostCreate(
            title="娱乐帖测试",
            content="这是娱乐内容，超过十个字符了。",
            category="fun"
        )
        PostService.create_post(db, test_user.id, data2)

        result = PostService.get_post_list(db, category="other")

        assert len(result["list"]) >= 1
        for post in result["list"]:
            assert post["category"] == "other"

    def test_get_post_list_with_user_filter(self, db, test_user):
        """测试按用户筛选帖子"""
        data = PostCreate(
            title="用户筛选测试",
            content="这是测试内容，超过十个字符了。"
        )
        PostService.create_post(db, test_user.id, data)

        result = PostService.get_post_list(db, user_id=test_user.id)

        assert len(result["list"]) >= 1
        for post in result["list"]:
            assert post["user_id"] == test_user.id

    def test_get_post_list_sort_newest(self, db, test_user):
        """测试最新排序"""
        import time
        data1 = PostCreate(
            title="第一个帖子测试",
            content="这是第一个帖子的内容，足够长了。"
        )
        PostService.create_post(db, test_user.id, data1)
        time.sleep(0.1)

        data2 = PostCreate(
            title="第二个帖子测试",
            content="这是第二个帖子的内容，足够长了。"
        )
        PostService.create_post(db, test_user.id, data2)

        result = PostService.get_post_list(db, sort="newest")

        assert len(result["list"]) >= 2
        assert result["list"][0]["title"] == "第二个帖子测试"

    def test_update_post_success(self, db, test_user):
        """测试更新帖子成功"""
        data = PostCreate(
            title="原标题测试",
            content="原始内容，必须超过十个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        update_data = PostUpdate(
            title="新标题测试",
            content="更新后的内容，超过十个字符。"
        )
        updated = PostService.update_post(db, post.id, test_user.id, update_data)

        assert updated.title == "新标题测试"
        assert updated.content == "更新后的内容，超过十个字符。"

    def test_update_post_unauthorized(self, db, test_user):
        """测试无权更新他人帖子"""
        data = PostCreate(
            title="他人帖子测试",
            content="这是他人创建的帖子，超过十个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 直接创建第二个用户
        user2 = User(
            username="user2",
            email="user2@example.com",
            password_hash="plain:123456",
            nickname="user2",
            is_verified=True,
        )
        db.add(user2)
        db.commit()
        db.refresh(user2)

        update_data = PostUpdate(title="恶意修改测试")
        with pytest.raises(HTTPException) as exc:
            PostService.update_post(db, post.id, user2.id, update_data)
        assert exc.value.status_code == 403

    def test_delete_post_success(self, db, test_user):
        """测试删除帖子成功"""
        data = PostCreate(
            title="待删除帖子测试",
            content="这个帖子将被删除，超过十个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        PostService.delete_post(db, post.id, test_user.id)

        from app.models.post import Post
        deleted_post = db.query(Post).filter(Post.id == post.id).first()
        assert deleted_post.is_deleted is True

    def test_delete_post_unauthorized(self, db, test_user):
        """测试无权删除他人帖子"""
        data = PostCreate(
            title="他人帖子测试",
            content="这是他人的帖子，超过十个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        # 直接创建第二个用户
        user2 = User(
            username="user3",
            email="user3@example.com",
            password_hash="plain:123456",
            nickname="user3",
            is_verified=True,
        )
        db.add(user2)
        db.commit()
        db.refresh(user2)

        with pytest.raises(HTTPException) as exc:
            PostService.delete_post(db, post.id, user2.id)
        assert exc.value.status_code == 403

    def test_like_post_success(self, db, test_user):
        """测试点赞帖子成功"""
        data = PostCreate(
            title="点赞测试帖子",
            content="这个帖子将被点赞，超过十个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        PostService.like_post(db, post.id, test_user.id)

        from app.models.post import Post
        updated_post = db.query(Post).filter(Post.id == post.id).first()
        assert updated_post.like_count == 1

    def test_like_post_already_liked(self, db, test_user):
        """测试重复点赞"""
        data = PostCreate(
            title="重复点赞测试",
            content="这个帖子将被重复点赞，超过十个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        PostService.like_post(db, post.id, test_user.id)

        with pytest.raises(HTTPException) as exc:
            PostService.like_post(db, post.id, test_user.id)
        assert exc.value.status_code == 400

    def test_unlike_post_success(self, db, test_user):
        """测试取消点赞成功"""
        data = PostCreate(
            title="取消点赞测试",
            content="这个帖子将被点赞然后取消，超过十个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        PostService.like_post(db, post.id, test_user.id)
        PostService.unlike_post(db, post.id, test_user.id)

        from app.models.post import Post
        updated_post = db.query(Post).filter(Post.id == post.id).first()
        assert updated_post.like_count == 0

    def test_bookmark_post_success(self, db, test_user):
        """测试收藏帖子成功"""
        data = PostCreate(
            title="收藏测试帖子",
            content="这个帖子将被收藏，超过十个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        PostService.bookmark_post(db, post.id, test_user.id)

        from app.models.post import Post
        updated_post = db.query(Post).filter(Post.id == post.id).first()
        assert updated_post.bookmark_count == 1

    def test_bookmark_post_already_bookmarked(self, db, test_user):
        """测试重复收藏"""
        data = PostCreate(
            title="重复收藏测试",
            content="这个帖子将被重复收藏，超过十个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        PostService.bookmark_post(db, post.id, test_user.id)

        with pytest.raises(HTTPException) as exc:
            PostService.bookmark_post(db, post.id, test_user.id)
        assert exc.value.status_code == 400

    def test_unbookmark_post_success(self, db, test_user):
        """测试取消收藏成功"""
        data = PostCreate(
            title="取消收藏测试",
            content="这个帖子将被收藏然后取消，超过十个字符。"
        )
        post = PostService.create_post(db, test_user.id, data)

        PostService.bookmark_post(db, post.id, test_user.id)
        PostService.unbookmark_post(db, post.id, test_user.id)

        from app.models.post import Post
        updated_post = db.query(Post).filter(Post.id == post.id).first()
        assert updated_post.bookmark_count == 0

    def test_get_user_bookmarks_success(self, db, test_user):
        """测试获取用户收藏列表"""
        for i in range(3):
            data = PostCreate(
                title=f"收藏帖子{i}号测试",
                content=f"这是第{i}个被收藏的帖子，超过十个字符。"
            )
            post = PostService.create_post(db, test_user.id, data)
            PostService.bookmark_post(db, post.id, test_user.id)

        result = PostService.get_user_bookmarks(db, test_user.id)

        assert result["total"] >= 3
        assert len(result["list"]) >= 3

    def test_get_post_list_with_following_sort(self, db, test_user):
        """测试关注排序（没有关注时返回空列表）"""
        result = PostService.get_post_list(db, sort="following", current_user_id=test_user.id)

        assert result["list"] == []
        assert result["total"] == 0

    def test_get_post_list_following_without_user(self, db):
        """测试关注排序但未登录"""
        result = PostService.get_post_list(db, sort="following", current_user_id=None)

        assert result["list"] == []
        assert result["total"] == 0
        assert result["has_more"] is False