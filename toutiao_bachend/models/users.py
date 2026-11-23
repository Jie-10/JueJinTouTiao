from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String
from models.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "user"
    # 创建索引：username 和 phone 都是唯一索引，加速登录、查重场景的查询
    __table_args__ = (
        Index('username_UNIQUE', 'username', unique=True),  # 用户名唯一索引
        Index('phone_UNIQUE', 'phone', unique=True),  # 手机号唯一索引
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(50), nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码（加密存储）")
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="头像URL")
    gender: Mapped[Optional[str]] = mapped_column(Enum('male', 'female', 'unknown'), default='unknown', nullable=True, comment="性别")
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="个人简介")
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="手机号")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, phone={self.phone})>"


class UserToken(Base):
    __tablename__ = "user_token"
    # 创建索引：校验 token 时按 user_id 高频查询；token 本身唯一
    __table_args__ = (
        Index('fk_user_token_user_idx', 'user_id'),  # 对应数据库里的普通索引
        Index('token_UNIQUE', 'token', unique=True),  # 对应数据库里的唯一索引
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="令牌ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False, comment="用户ID")
    token: Mapped[str] = mapped_column(String(255), nullable=False, comment="令牌值")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")
    # user_token 表没有 updated_at 字段，所以这里单独声明 created_at，不继承 TimestampMixin
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")

    def __repr__(self) -> str:
        return f"<UserToken(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>"

