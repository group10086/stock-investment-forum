"""敏感词模型"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class SensitiveWord(Base):
    __tablename__ = "sensitive_words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), unique=True, nullable=False)
    replacement = Column(String(100), default="***")
    created_at = Column(DateTime, default=datetime.now)
