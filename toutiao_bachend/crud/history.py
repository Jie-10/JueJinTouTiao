# 浏览历史表的数据访问：history 表（与 news 表联查）
# 本层只做纯 SQL 操作；业务规则与模型组装在 services 层
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, func
from models.history import History
from models.news import News


# 判断浏览记录是否存在
async def is_history_exists(db: AsyncSession, user_id: int, news_id: int):
    result = await db.execute(select(History).where(History.user_id == user_id, History.news_id == news_id))
    return result.scalar_one_or_none() is not None


# 添加浏览历史：同一新闻重复浏览时先删旧记录再插入
# 去重设计：history 表没有唯一约束，靠"先删后插"保证同一新闻只留一条，
# 且新记录时间最新、排在列表最前
async def add_history(db: AsyncSession, user_id: int, news_id: int):
    await db.execute(delete(History).where(History.user_id == user_id, History.news_id == news_id))
    db_history = History(user_id=user_id, news_id=news_id)
    db.add(db_history)
    await db.commit()
    await db.refresh(db_history)
    return db_history


# 查询浏览历史列表（历史表 join 新闻表），返回行数据与总数
async def get_history_list(db: AsyncSession, user_id: int, skip: int, limit: int):
    # join 联查的原因：历史列表要展示新闻的标题/封面等字段，这些都在 news 表
    # 两表都有 id，重复字段用 label 取别名区分（如 view_time）
    stmt = (
        select(
            News.id.label("id"),
            News.title.label("title"),
            News.description.label("description"),
            News.image.label("image"),
            News.author.label("author"),
            News.views.label("views"),
            News.publish_time.label("publish_time"),
            History.view_time.label("view_time"),
        )
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    rows = result.all()
    total = await db.scalar(select(func.count(History.id)).where(History.user_id == user_id))
    return rows, total


# 删除单条浏览历史，返回是否真正删除
async def remove_history(db: AsyncSession, user_id: int, news_id: int):
    result = await db.execute(
        delete(History).where(History.user_id == user_id, History.news_id == news_id)
    )
    await db.commit()
    return result.rowcount > 0


# 清空浏览历史，返回删除条数
async def clear_history(db: AsyncSession, user_id: int):
    result = await db.execute(delete(History).where(History.user_id == user_id))
    await db.commit()
    return result.rowcount
