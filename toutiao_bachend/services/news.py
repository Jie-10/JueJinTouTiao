from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from cache import news_cache
from crud import news as news_crud
from schemas.news import NewsDetailResponse, RelatedNewsItem


# 获取分类列表
# 缓存策略（旁路缓存 Cache-Aside）：
#   1. 先查缓存：命中直接返回，完全不碰数据库
#   2. 缓存未命中：查数据库
#   3. 查库有结果：回填缓存（序列化成 JSON 字符串），下次请求即可命中
# 旁路缓存的取舍：缓存与数据库是"懒同步"关系；
# 写缓存失败只影响性能、不影响正确性（下次仍会查库）
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 第 1 步：尝试从 Redis 读取
    cached_categories = await news_cache.get_cache_categories()
    if cached_categories:
        return cached_categories
    # 第 2 步：缓存未命中，查数据库
    categories = await news_crud.get_categories(db, skip, limit)
    # 第 3 步：查到数据后回填缓存（ORM 对象 -> 可序列化的字典列表）
    if categories:
        categories = jsonable_encoder(categories)
        await news_cache.set_cache_categories(categories)
    return categories


# 获取新闻列表
# 逻辑链：分页换算 -> 旁路缓存 -> 统计总量 -> 计算是否还有更多
async def get_news_list(db: AsyncSession, category_id: int, page: int, page_size: int):
    # 第 1 步：页码换算为 SQL 偏移量（skip = 前面跳过多少条）
    skip = (page - 1) * page_size
    # 第 2 步：旁路缓存。缓存 key 由"分类id:页码:每页条数"组成，
    # 每个分类的每一页都有独立缓存，互不影响
    cached_news = await news_cache.get_cache_news_list(category_id, page, page_size)
    if cached_news:
        news_list = cached_news
    else:
        news_list = await news_crud.get_news_list(db, category_id, skip, page_size)
        if news_list:
            news_list = jsonable_encoder(news_list)
            await news_cache.set_cache_news_list(category_id, page, page_size, news_list)
    # 第 3 步：统计该分类新闻总量（总量不走缓存，保证准确）
    total = await news_crud.get_news_count(db, category_id)
    # 第 4 步：判断是否还有下一页：已展示条数 < 总量
    has_more = total > page * page_size
    return news_list, total, has_more


# 获取新闻详情
# 编排逻辑链：查询详情 -> 浏览量+1 -> 查询相关新闻 -> 组装响应模型
# 这是"一个接口、三次数据库操作"的典型编排场景，
# 分层重构前这些步骤散落在路由函数里，现在统一收口到 service 层
async def get_news_detail(db: AsyncSession, news_id: int):
    # 第 1 步：查询详情，查不到直接抛 404 业务错误
    news_detail = await news_crud.get_news_detail(db, news_id)
    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")
    # 第 2 步：浏览量 +1（每次打开详情页都计一次）
    if not await news_crud.increase_news_views(db, news_id):
        raise HTTPException(status_code=404, detail="Failed to increase views")
    # 第 3 步：查询同分类下的相关新闻（按浏览量、发布时间倒序，排除自身）
    related_news = await news_crud.get_related_news(db, news_id, news_detail.category_id, 5)
    # 第 4 步：组装响应模型（ORM 对象 -> Pydantic 模型），
    # 序列化时字段别名自动输出前端需要的驼峰键 publishTime/categoryId/relatedNews
    related_items = [RelatedNewsItem.model_validate(item) for item in related_news]
    return NewsDetailResponse(
        id=news_detail.id,
        title=news_detail.title,
        content=news_detail.content,
        image=news_detail.image,
        author=news_detail.author,
        publish_time=news_detail.publish_time,
        category_id=news_detail.category_id,
        views=news_detail.views,
        related_news=related_items,
    )
