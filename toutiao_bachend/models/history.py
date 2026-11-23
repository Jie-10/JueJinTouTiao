from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class History(Base):
    __tablename__ = "history"
    # 创建索引：按用户查询历史、按新闻查询历史、按浏览时间倒序都是高频场景
    __table_args__ = (
        Index('fk_history_user_idx', 'user_id'),
        Index('fk_history_news_idx', 'news_id'),
        Index('idx_view_time', 'view_time'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="历史ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey("news.id"), nullable=False, comment="新闻ID")
    # 浏览历史只有浏览时间，无更新场景，所以单独声明 view_time，不继承 TimestampMixin
    view_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="浏览时间")

    def __repr__(self) -> str:
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"
