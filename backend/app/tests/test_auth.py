"""认证模块 - 单元测试"""

import pytest
from fastapi import status

from app.models.user import User
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin


class TestAuthService:
    """认证服务测试"""

    def test_register_success(self, db):
        """测试注册成功"""
        data = UserCreate(
            username="newuser",
            email="new@example.com",
            password="password123"
        )
        result = AuthService.register(db, data)

        assert "user" in result
        assert "token" in result
        assert result["user"].username == "newuser"
        assert result["user"].email == "new@example.com"

    def test_register_duplicate_username(self, db):
        """测试重复用户名注册"""
        data = UserCreate(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        AuthService.register(db, data)

        data2 = UserCreate(
            username="testuser",
            email="other@example.com",
            password="password123"
        )
        with pytest.raises(Exception):
            AuthService.register(db, data2)

    def test_register_duplicate_email(self, db):
        """测试重复邮箱注册"""
        data1 = UserCreate(
            username="user1",
            email="same@example.com",
            password="password123"
        )
        AuthService.register(db, data1)

        data2 = UserCreate(
            username="user2",
            email="same@example.com",
            password="password123"
        )
        with pytest.raises(Exception):
            AuthService.register(db, data2)

    def test_login_success(self, db):
        """测试登录成功"""
        # 先注册
        register_data = UserCreate(
            username="loginuser",
            email="login@example.com",
            password="password123"
        )
        AuthService.register(db, register_data)

        # 再登录
        login_data = UserLogin(
            email="login@example.com",
            password="password123"
        )
        result = AuthService.login(db, login_data)

        assert "user" in result
        assert "token" in result
        assert result["user"].username == "loginuser"

    def test_login_wrong_password(self, db):
        """测试错误密码登录"""
        register_data = UserCreate(
            username="loginuser2",
            email="login2@example.com",
            password="password123"
        )
        AuthService.register(db, register_data)

        login_data = UserLogin(
            email="login2@example.com",
            password="wrongpassword"
        )
        with pytest.raises(Exception):
            AuthService.login(db, login_data)

    def test_login_nonexistent_user(self, db):
        """测试不存在的用户登录"""
        login_data = UserLogin(
            email="nonexistent@example.com",
            password="password123"
        )
        with pytest.raises(Exception):
            AuthService.login(db, login_data)


class TestAuthAPI:
    """认证API测试"""

    def test_register_api(self, client, test_user_data):
        """测试注册API"""
        response = client.post("/api/auth/register", json=test_user_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "注册成功"
        assert "token" in data["data"]

    def test_login_api(self, client, test_user_data):
        """测试登录API"""
        # 先注册
        client.post("/api/auth/register", json=test_user_data)

        # 再登录
        login_data = {
            "email": test_user_data["email"],
            "password": test_user_data["password"]
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "登录成功"
        assert "token" in data["data"]

    def test_login_invalid_credentials(self, client):
        """测试无效凭证登录"""
        login_data = {
            "email": "wrong@example.com",
            "password": "wrongpass"
        }
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
