# 用户与令牌表的数据访问：user 表、user_token 表
# 本层只做纯 SQL 操作；密码加密、token 生成、过期校验等业务规则在 services 层
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.users import User, UserToken


# 根据用户名查询用户
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


# 根据用户ID查询用户
async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


# 创建用户（密码哈希由 service 层处理，本层只做写入）
async def create_user(db: AsyncSession, username: str, hashed_password: str):
    user = User(username=username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # 刷新以取回数据库生成的 id 等字段
    return user


# 根据 token 值查询令牌记录（是否过期由 service 层判断）
async def get_token_record(db: AsyncSession, token: str):
    result = await db.execute(select(UserToken).where(UserToken.token == token))
    return result.scalar_one_or_none()


# 写入令牌：已有记录则更新 token 值与过期时间，否则新建
# 这是"一人一 token"不变量的落地位置：
# 按 user_id 查已有记录最多一条，因此可用 scalar_one_or_none()
async def upsert_token(db: AsyncSession, user_id: int, token: str, expires_at):
    result = await db.execute(select(UserToken).where(UserToken.user_id == user_id))
    user_token = result.scalar_one_or_none()
    if user_token:
        # 已有记录：刷新 token 值并续期（覆盖旧 token，旧登录态随之失效）
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
    # commit 放在 if/else 之外，保证两个分支都统一提交
    await db.commit()
    return user_token


# 按用户ID更新资料字段，返回更新后的用户
async def update_user(db: AsyncSession, user_id: int, values: dict):
    await db.execute(update(User).where(User.id == user_id).values(**values))
    await db.commit()
    return await get_user_by_id(db, user_id)


# 按用户ID更新密码哈希，返回更新后的用户
async def update_password(db: AsyncSession, user_id: int, hashed_password: str):
    await db.execute(update(User).where(User.id == user_id).values(password=hashed_password))
    await db.commit()
    return await get_user_by_id(db, user_id)
