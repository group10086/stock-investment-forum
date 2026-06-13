"""管理运营模块 - 单元测试"""

import pytest

from app.services.auth_service import AuthService
from app.services.admin_service import AdminService
from app.models.sensitive_word import SensitiveWord
from app.schemas.user import UserCreate
from app.utils.sensitive_filter import SensitiveFilter


class TestSensitiveFilter:
    """敏感词过滤器测试"""

    def test_build_and_filter(self):
        """测试构建和过滤"""
        sf = SensitiveFilter()
        sf.build(["赌博", "色情", "毒品"])

        result = sf.filter("我喜欢赌博和色情内容")
        assert "***" in result
        assert "赌博" not in result
        assert "色情" not in result

    def test_contains_sensitive(self):
        """测试检测敏感词"""
        sf = SensitiveFilter()
        sf.build(["毒品", "暴力"])

        assert sf.contains_sensitive("远离毒品")
        assert sf.contains_sensitive("禁止暴力")
        assert not sf.contains_sensitive("正常内容")

    def test_find_all(self):
        """测试查找所有敏感词"""
        sf = SensitiveFilter()
        sf.build(["赌博", "色情"])

        result = sf.find_all("赌博和色情都是有害的")
        assert len(result) == 2
        assert result[0][0] == "赌博"
        assert result[1][0] == "色情"

    def test_no_sensitive_words(self):
        """测试无敏感词"""
        sf = SensitiveFilter()
        sf.build(["赌博"])

        result = sf.filter("这是一段正常的内容")
        assert result == "这是一段正常的内容"

        assert not sf.contains_sensitive("正常内容")

    def test_empty_filter(self):
        """测试未初始化的过滤器"""
        sf = SensitiveFilter()
        assert sf.filter("任何内容") == "任何内容"
        assert not sf.contains_sensitive("任何内容")


class TestAdminService:
    """管理服务测试"""

    @pytest.fixture
    def setup_admin(self, db):
        """创建管理员"""
        from app.models.user import User
        from passlib.hash import bcrypt
        from datetime import datetime

        admin = User(
            username="testadmin",
            email="testadmin@example.com",
            password_hash=bcrypt.hash("admin123"),
            nickname="测试管理员",
            is_admin=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return admin

    def test_add_sensitive_word(self, db, setup_admin):
        """测试添加敏感词"""
        sw = AdminService.add_sensitive_word(db, "测试敏感词", "***")
        assert sw.word == "测试敏感词"
        assert sw.replacement == "***"

    def test_get_sensitive_words(self, db, setup_admin):
        """测试获取敏感词列表"""
        AdminService.add_sensitive_word(db, "敏感词1")
        AdminService.add_sensitive_word(db, "敏感词2")

        words = AdminService.get_sensitive_words(db)
        assert len(words) == 2

    def test_delete_sensitive_word(self, db, setup_admin):
        """测试删除敏感词"""
        sw = AdminService.add_sensitive_word(db, "待删除词")
        AdminService.delete_sensitive_word(db, sw.id)

        words = AdminService.get_sensitive_words(db)
        assert len(words) == 0

    def test_mute_user(self, db, setup_admin):
        """测试禁言用户"""
        user_data = UserCreate(
            username="muteduser",
            email="muted@example.com",
            password="password123"
        )
        user = AuthService.register(db, user_data)["user"]

        AdminService.mute_user(db, user.id, days=7)

        db.refresh(user)
        assert user.is_muted == True
        assert user.muted_until is not None

    def test_unmute_user(self, db, setup_admin):
        """测试解除禁言"""
        user_data = UserCreate(
            username="unmuteduser",
            email="unmuted@example.com",
            password="password123"
        )
        user = AuthService.register(db, user_data)["user"]

        AdminService.mute_user(db, user.id, days=7)
        AdminService.unmute_user(db, user.id)

        db.refresh(user)
        assert user.is_muted == False
        assert user.muted_until is None

    def test_create_report(self, db, setup_admin):
        """测试创建举报"""
        report = AdminService.create_report(
            db,
            reporter_id=setup_admin.id,
            target_type="post",
            target_id=1,
            reason="违规内容"
        )
        assert report.target_type == "post"
        assert report.reason == "违规内容"
        assert report.status == "pending"
