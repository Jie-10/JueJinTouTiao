import starlette.status as status
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud import users as users_crud
from schemas.users import UserRegister, UserUpdateRequest
from services import auth
from utils import security


# 注册
# 逻辑链：校验用户名唯一 -> 密码加密 -> 创建用户 -> 签发令牌
async def register(db: AsyncSession, user_data: UserRegister):
    # 第 1 步：查重——提前给出友好提示；
    # 数据库的 username 唯一索引是最后防线：并发注册同名用户时，
    # 由 IntegrityError -> 全局异常处理器兜底返回 400
    existing_user = await users_crud.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    # 第 2 步：密码加密后才入库，数据库不存明文
    hashed_password = security.get_hash_password(user_data.password)
    # 第 3 步：创建用户记录
    new_user = await users_crud.create_user(db, user_data.username, hashed_password)
    # 第 4 步：为新用户签发令牌（注册成功即视为登录成功，前端无需二次登录）
    token = await auth.create_token(db, new_user.id)
    return token, new_user


# 登录
# 逻辑链：校验账号密码 -> 签发令牌
async def login(db: AsyncSession, username: str, password: str):
    # 第 1 步：认证。用户名不存在与密码错误统一返回同一条错误，
    # 避免向攻击者暴露"哪个用户名是真实存在的"
    user = await auth.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    # 第 2 步：签发新令牌。按"一人一 token"策略，旧 token 被覆盖后即失效
    token = await auth.create_token(db, user.id)
    return token, user


# 更新用户资料
# 逻辑链：过滤未提交字段 -> 按用户ID更新 -> 返回更新后的用户
async def update_user_info(db: AsyncSession, user, user_data: UserUpdateRequest):
    # exclude_unset：只更新请求体里实际出现的字段，未提交的字段保持原值
    # exclude_none：显式传 null 的字段也不更新，避免把已有资料清空
    values = user_data.model_dump(exclude_unset=True, exclude_none=True)
    # 用 user.id（主键）定位而不是 username：当前用户来自认证依赖，id 更精确
    return await users_crud.update_user(db, user.id, values)


# 修改密码
# 逻辑链：校验旧密码 -> 加密新密码 -> 更新
async def change_password(db: AsyncSession, user, old_password: str, new_password: str):
    # 第 1 步：校验旧密码。直接用认证依赖注入的 user 对象比对，
    # 省去一次数据库查询（verify_password 内部用 bcrypt 校验）
    if not security.verify_password(old_password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="旧密码错误")
    # 第 2 步：新密码同样加密存储
    hashed_new_password = security.get_hash_password(new_password)
    # 第 3 步：按用户ID更新密码
    await users_crud.update_password(db, user.id, hashed_new_password)
