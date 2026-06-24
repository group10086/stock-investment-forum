"""附件模型"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey
from app.database import Base


class Attachment(Base):
    """帖子/评论附件"""
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target_type = Column(String(20), nullable=False)  # post / comment
    target_id = Column(Integer, nullable=False)
    filename = Column(String(255), nullable=False)
    filepath = Column(String(500), nullable=False)
    filesize = Column(BigInteger, default=0)
    filetype = Column(String(50), default="")
    created_at = Column(DateTime, default=datetime.now)
