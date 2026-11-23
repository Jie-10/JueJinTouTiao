import datetime
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from crud import users as users_crud
from utils import security


# 校验用户名与密码，认证成功返回用户对象，失败返回 None
# 逻辑链：按用户名查用户 -> 用户不存在直接失败 -> bcrypt 校验密码 -> 返回结果
async def authenticate_user(db: AsyncSession, username: str, password: str):
    # 第 1 步：按用户名查询用户
    user = await users_crud.get_user_by_username(db, username)
    if not user:
        return None
    # 第 2 步：比对密码。数据库中存的是 bcrypt 哈希（自带随机盐），
    # verify_password 内部完成加盐比对，无需手动处理盐值
    if not security.verify_password(password, user.password):
        return None
    return user


# 为用户签发新令牌
# 设计要点（一人一 token 不变量）：
# 1. token 用 uuid4 生成，随机性强，客户端无法猜测
# 2. 有效期 7 天，过期时间随 token 一起入库，校验时以库中值为准
# 3. 复用策略：一个用户同时只保留一条 token 记录
#    - 已有记录 -> 刷新 token 值并续期（重新登录会使旧 token 失效）
#    - 没有记录 -> 新建
#    该不变量是 get_user_by_token 用 scalar_one_or_none() 查询的前提
async def create_token(db: AsyncSession, user_id: int) -> str:
    token = str(uuid.uuid4())
    expires_at = datetime.datetime.now() + datetime.timedelta(days=7)
    await users_crud.upsert_token(db, user_id, token, expires_at)
    return token


# 根据 token 查询有效用户：令牌不存在或已过期返回 None
# 逻辑链（为什么是两步查询）：
#   expires_at 字段在 user_token 表上，User 实体上没有该属性，
#   所以必须先查令牌记录做过期判断，再按 user_id 反查用户实体
async def get_user_by_token(db: AsyncSession, token: str):
    # 第 1 步：按 token 值查询令牌记录
    db_token = await users_crud.get_token_record(db, token)
    # 令牌不存在，或已过有效期 -> 视为无效 token
    if not db_token or db_token.expires_at < datetime.datetime.now():
        return None
    # 第 2 步：按令牌中的 user_id 查询用户实体
    return await users_crud.get_user_by_id(db, db_token.user_id)
