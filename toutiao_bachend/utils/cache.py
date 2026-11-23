from config.redis_conf import redis_client


# 缓存操作异常：缓存读写发生异常时统一抛出，方便调用方捕获判断
class CacheError(Exception):
    pass


# 设置缓存并指定过期时间（秒）
async def setex(key: str, expire: int, value: str):
    try:
        await redis_client.setex(key, expire, value)
    except Exception as e:
        raise CacheError(f"缓存写入失败：key={key}，原因：{e}") from e


# 获取缓存值，缓存不存在时返回 None
async def get(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        raise CacheError(f"缓存读取失败：key={key}，原因：{e}") from e


# 删除指定的缓存键
async def delete(key: str):
    try:
        await redis_client.delete(key)
    except Exception as e:
        raise CacheError(f"缓存删除失败：key={key}，原因：{e}") from e


# 检查缓存键是否存在，返回布尔值
async def exists(key: str) -> bool:
    try:
        return bool(await redis_client.exists(key))
    except Exception as e:
        raise CacheError(f"缓存查询失败：key={key}，原因：{e}") from e
