# 新闻与分类表的数据访问：news_category 表、news 表
# 本层只做纯 SQL 操作；缓存策略、分页计算在 services 层
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News


# 查询新闻分类（纯数据库查询，缓存策略由 service 层处理）
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()


# 查询指定分类下的新闻列表（纯数据库查询）
async def get_news_list(db: AsyncSession, category_id: int, skip: int, limit: int):
    stmt = select(News).where(News.category_id == category_id)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return result.scalars().all()


# 统计指定分类下的新闻总数
async def get_news_count(db: AsyncSession, category_id: int):
    result = await db.execute(select(func.count(News.id)).where(News.category_id == category_id))
    return result.scalar_one()


# 查询新闻详情
async def get_news_detail(db: AsyncSession, news_id: int):
    result = await db.execute(select(News).where(News.id == news_id))
    return result.scalar_one_or_none()


# 浏览量 +1，返回是否命中记录
async def increase_news_views(db: AsyncSession, news_id: int) -> bool:
    # News.views + 1 是 SQL 层面的原子自增，不依赖先读后写，并发安全
    result = await db.execute(update(News).where(News.id == news_id).values(views=News.views + 1))
    await db.commit()
    return result.rowcount > 0


# 查询同分类下的相关新闻（排除自身，按浏览量与发布时间排序）
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, limit: int):
    stmt = select(News).where(
        News.id != news_id,
        News.category_id == category_id
    ).order_by(News.views.desc(), News.publish_time.desc()).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
