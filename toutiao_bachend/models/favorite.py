from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Favorite(Base):
    __tablename__ = "favorite"
    # 创建索引
    # UniqueConstraint: 唯一约束, 同一用户不能重复收藏同一新闻
    __table_args__ = (
        UniqueConstraint('user_id', 'news_id', name='user_news_unique'),
        Index('fk_favorite_user_idx', 'user_id'),
        Index('fk_favorite_news_idx', 'news_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="收藏ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey("news.id"), nullable=False, comment="新闻ID")
    # 收藏行为只有创建时间，无更新场景，所以单独声明 created_at，不继承 TimestampMixin
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="收藏时间")

    def __repr__(self) -> str:
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"
