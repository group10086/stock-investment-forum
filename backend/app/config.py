"""配置文件"""

import os
from datetime import timedelta


class Settings:
    # 数据库配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/stock_forum"
    )

    # JWT配置
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "stock-forum-jwt-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # 应用配置
    APP_NAME: str = "股票基金投资论坛 API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:8000"]

    # 分页
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100


settings = Settings()
