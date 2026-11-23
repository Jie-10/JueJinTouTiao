from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """全项目唯一的 ORM 基类，所有模型都必须继承它，
    否则各模型的 metadata 注册表相互独立，外键跨模型解析会报 NoReferencedTableError"""
    pass


class TimestampMixin:
    """通用时间戳字段（created_at / updated_at），需要这两个字段的表可继承"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间",
    )
