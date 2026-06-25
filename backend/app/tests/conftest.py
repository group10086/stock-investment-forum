"""Pytest 测试配置文件"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# 导入所有模型
from app.models import User, Post, Comment, Follow, PostLike, Bookmark, CommentLike, Message, Group, GroupMember, Report, SensitiveWord, StarFollow, Attachment


# 测试数据库配置（使用 SQLite 内存数据库）
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """创建测试数据库会话，每个测试函数结束后回滚"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """创建测试客户端，覆盖数据库依赖"""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db):
    """直接创建测试用户（明文密码，不加密）"""
    user = User(
        username="testuser",
        email="test@example.com",
        password_hash="plain:123456",
        nickname="testuser",
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_user_token(db, test_user):
    """获取测试用户的JWT token"""
    from app.utils.jwt_handler import create_access_token
    return create_access_token({"user_id": test_user.id})


@pytest.fixture(scope="function")
def auth_headers(test_user_token):
    """认证请求头"""
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture(scope="function")
def test_post_data():
    """测试帖子数据"""
    return {
        "title": "测试帖子标题",
        "content": "这是测试帖子的内容，长度应该大于10个字符。",
        "category": "tech",
        "tags": ["python", "测试"]
    }