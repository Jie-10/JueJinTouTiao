from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import favorite as favorite_crud
from schemas.favorite import FavoriteListItem


# 查询收藏状态：当前用户是否收藏了这条新闻
# 无业务规则，直接透传 crud 的布尔查询结果
async def check_favorite(db: AsyncSession, user_id: int, news_id: int):
    return await favorite_crud.is_favorite(db, user_id, news_id)


# 添加收藏
# 数据库兜底设计：
# - user_id/news_id 的外键约束保证不会收藏到不存在的用户或新闻
# - user_id+news_id 联合唯一约束拦截重复收藏，
#   违反时抛 IntegrityError -> 全局异常处理器 -> 统一返回 400 提示
async def add_favorite(db: AsyncSession, user_id: int, news_id: int):
    return await favorite_crud.add_favorite(db, user_id, news_id)


# 取消收藏
# 业务规则：未收藏时直接报错，而不是静默成功
# 设计取舍：把"取消了没收藏过的新闻"这种异常操作暴露给调用方，
# 便于前端发现状态不同步问题
async def remove_favorite(db: AsyncSession, user_id: int, news_id: int):
    # 第 1 步：先查收藏状态，未收藏则抛业务错误
    if not await favorite_crud.is_favorite(db, user_id, news_id):
        raise HTTPException(status_code=404, detail="尚未收藏该新闻")
    # 第 2 步：确认已收藏，执行删除
    return await favorite_crud.remove_favorite(db, user_id, news_id)


# 收藏列表
# 逻辑链：分页换算 -> 联表查询 -> 组装列表项模型 -> 计算是否还有更多
async def get_favorite_list(db: AsyncSession, user_id: int, page: int, page_size: int):
    # 第 1 步：页码换算为 SQL 偏移量
    skip = (page - 1) * page_size
    # 第 2 步：收藏表 join 新闻表联查，同时拿到行数据与总收藏数
    rows, total = await favorite_crud.get_favorite_list(db, user_id, skip, page_size)
    # 第 3 步：把原始查询行组装成 Pydantic 列表项模型（序列化时自动转驼峰键）
    favorites = [FavoriteListItem(**dict(row._mapping)) for row in rows]
    # 第 4 步：判断是否还有下一页
    has_more = total > page * page_size
    return favorites, total, has_more


# 清空收藏：按 user_id 删除该用户全部收藏记录，返回删除条数
async def clear_favorites(db: AsyncSession, user_id: int):
    return await favorite_crud.clear_favorites(db, user_id)
