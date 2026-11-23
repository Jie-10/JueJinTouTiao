import json
from typing import Any, Dict, List, Optional

from utils.cache import get, setex, delete

# 过期时间策略（秒）：数据越稳定，缓存越持久
# 分类、配置 7200；列表：600；详情：1800；验证码：120
# 不同数据使用不同过期时间，避免所有 key 同时过期引起缓存雪崩
CATEGORIES_EXPIRE = 7200
NEWS_LIST_EXPIRE = 600

# 缓存 key 约定
CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news_list:"


# 通用缓存写入：序列化后存储，带过期时间
async def set_cache(key: str, data: Any, expire: int):
    # 字典列表不能直接存 Redis，先序列化成 JSON 字符串
    await setex(key, expire, json.dumps(data, ensure_ascii=False))


# 通用缓存读取：反序列化，未命中返回 None
async def get_cache(key: str):
    cached = await get(key)
    if cached is None:
        return None
    return json.loads(cached)


# 写入新闻分类缓存：缓存的数据，过期时间
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = CATEGORIES_EXPIRE):
    await set_cache(CATEGORIES_KEY, data, expire)


# 读取新闻分类缓存
async def get_cache_categories():
    return await get_cache(CATEGORIES_KEY)


# 删除新闻分类缓存（分类数据发生变化时调用，保证下次读取查库拿到最新数据）
async def delete_cache_categories():
    await delete(CATEGORIES_KEY)


# 写入缓存-新闻列表 key = news_list:分类id:页码:每页数量 + 列表数据 + 过期时间
async def set_cache_news_list(
        category_id: Optional[int],
        page: int,
        size: int,
        news_list: List[Dict[str, Any]],
        expire: int = NEWS_LIST_EXPIRE
):
    # 调用封装的 Redis 的设置方法，存新闻列表到缓存
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await set_cache(key, news_list, expire)


# 读取缓存-新闻列表
async def get_cache_news_list(category_id: Optional[int], page: int, size: int):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{size}"
    return await get_cache(key)
