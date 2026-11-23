import redis.asyncio as aioredis

# Redis 连接URL（对应本机 Docker 容器 redis，端口 6379，使用 0 号库）
REDIS_URL = "redis://127.0.0.1:6379/0"

# 创建全局异步 Redis 客户端（内部自带连接池，自动复用连接，无需每次新建）
redis_client = aioredis.from_url(
    REDIS_URL,
    decode_responses=True,  # 返回结果自动解码为 str，省去手动 decode
)

# 依赖项，用于在接口中获取 Redis 客户端
async def get_redis():
    yield redis_client

# 关闭 Redis 连接池（应用关闭时调用）
async def close_redis():
    await redis_client.aclose()
