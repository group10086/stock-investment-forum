"""Pytest 测试配置文件"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.follow import Follow
from app.models.post_like import PostLike
from app.models.bookmark import Bookmark
from app.models.message import Message
from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.report import Report
from app.models.sensitive_word import SensitiveWord


# 测试数据库配置（使用独立的测试数据库）
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/stock_forum_test"

# 创建测试引擎
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """创建测试数据库会话，每个测试函数结束后回滚"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

    # 清理表
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
def test_user_data():
    """测试用户数据"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }


@pytest.fixture(scope="function")
def test_user(db, test_user_data):
    """创建测试用户并返回"""
    from app.services.auth_service import AuthService
    from app.schemas.user import UserCreate

    data = UserCreate(**test_user_data)
    result = AuthService.register(db, data)
    return result["user"]


@pytest.fixture(scope="function")
def test_user_token(db, test_user_data):
    """获取测试用户的JWT token"""
    from app.services.auth_service import AuthService
    from app.schemas.user import UserCreate, UserLogin

    register_data = UserCreate(**test_user_data)
    AuthService.register(db, register_data)

    login_data = UserLogin(
        email=test_user_data["email"],
        password=test_user_data["password"]
    )
    result = AuthService.login(db, login_data)
    return result["token"]


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