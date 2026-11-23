from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import history as history_crud
from schemas.history import HistoryListItem


# 添加浏览历史
# 设计要点（去重策略）：同一新闻重复浏览时，先删旧记录再插入新记录，
# 既避免同一新闻出现多条记录，又保证最新浏览的记录时间最新、排在列表最前
# （history 表没有唯一约束，靠这个"先删后插"实现同一新闻只留一条）
async def add_history(db: AsyncSession, user_id: int, news_id: int):
    return await history_crud.add_history(db, user_id, news_id)


# 浏览历史列表
# 逻辑链：分页换算 -> 联表查询 -> 组装列表项模型 -> 计算是否还有更多
async def get_history_list(db: AsyncSession, user_id: int, page: int, page_size: int):
    # 第 1 步：页码换算为 SQL 偏移量
    skip = (page - 1) * page_size
    # 第 2 步：历史表 join 新闻表联查，同时拿到行数据与总记录数
    rows, total = await history_crud.get_history_list(db, user_id, skip, page_size)
    # 第 3 步：把原始查询行组装成 Pydantic 列表项模型（序列化时自动转驼峰键）
    histories = [HistoryListItem(**dict(row._mapping)) for row in rows]
    # 第 4 步：判断是否还有下一页
    has_more = total > page * page_size
    return histories, total, has_more


# 删除单条浏览历史
# 业务规则：记录不存在时抛出业务错误，与"删除成功与否"明确区分，
# 便于前端感知数据状态
async def remove_history(db: AsyncSession, user_id: int, news_id: int):
    # 第 1 步：存在性校验，不存在则抛业务错误
    if not await history_crud.is_history_exists(db, user_id, news_id):
        raise HTTPException(status_code=404, detail="该浏览记录不存在")
    # 第 2 步：确认存在后删除
    return await history_crud.remove_history(db, user_id, news_id)


# 清空浏览历史：按 user_id 删除该用户全部浏览记录，返回删除条数
async def clear_history(db: AsyncSession, user_id: int):
    return await history_crud.clear_history(db, user_id)
