# 收藏表的数据访问：favorite 表（与 news 表联查）
# 本层只做纯 SQL 操作；业务规则与模型组装在 services 层
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, func
from models.favorite import Favorite
from models.news import News


# 判断用户是否已收藏某条新闻
async def is_favorite(db: AsyncSession, user_id: int, news_id: int):
    result = await db.execute(select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id))
    return result.scalar_one_or_none() is not None


# 新增收藏记录
# 重复收藏由数据库的 user_id+news_id 联合唯一约束拦截（抛出 IntegrityError）
async def add_favorite(db: AsyncSession, user_id: int, news_id: int):
    db_favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(db_favorite)
    await db.commit()
    await db.refresh(db_favorite)
    return db_favorite


# 删除收藏记录，返回是否真正删除
async def remove_favorite(db: AsyncSession, user_id: int, news_id: int):
    result = await db.execute(
        delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    )
    await db.commit()
    return result.rowcount > 0


# 查询收藏列表（收藏表 join 新闻表），返回行数据与总数
async def get_favorite_list(db: AsyncSession, user_id: int, skip: int, limit: int):
    # join 联查的原因：收藏列表要展示新闻的标题/封面等字段，这些都在 news 表
    # 两表都有 id/created_at，重复字段用 label 取别名区分（如 favorite_time）
    stmt = (
        select(
            News.id.label("id"),
            News.title.label("title"),
            News.description.label("description"),
            News.image.label("image"),
            News.author.label("author"),
            News.views.label("views"),
            News.publish_time.label("publish_time"),
            Favorite.created_at.label("favorite_time"),
        )
        .join(Favorite, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()
    total = await db.scalar(select(func.count(Favorite.id)).where(Favorite.user_id == user_id))
    return rows, total


# 清空收藏，返回删除条数
async def clear_favorites(db: AsyncSession, user_id: int):
    result = await db.execute(delete(Favorite).where(Favorite.user_id == user_id))
    await db.commit()
    return result.rowcount
