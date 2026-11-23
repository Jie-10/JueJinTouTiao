from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from models.users import User
from schemas.users import UserAuthData, UserChangePasswordRequest, UserInfoResponse, UserRegister, UserUpdateRequest
from services import users as user_service
from utils import response
from utils.auth import get_current_user

router = APIRouter(prefix='/api/user', tags=['user'])


@router.post('/register')
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    # 注册：校验用户名唯一 -> 创建用户 -> 签发令牌（编排在 service 层）
    token, user = await user_service.register(db, user_data)
    return response.success_response(
        message="注册成功",
        data=UserAuthData(token=token, user_info=UserInfoResponse.model_validate(user))
    )


@router.post('/login')
async def login(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    # 登录：校验账号密码 -> 签发令牌（编排在 service 层）
    token, user = await user_service.login(db, user_data.username, user_data.password)
    return response.success_response(
        message="登录成功",
        data=UserAuthData(token=token, user_info=UserInfoResponse.model_validate(user))
    )


# 根据 Token 查询用户：经认证依赖注入当前用户 -> 响应结果
@router.get('/info')
async def get_user_info(user: User = Depends(get_current_user)):
    return response.success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))


# 修改用户信息：认证依赖注入当前用户 -> 交给 service 更新 -> 响应结果
@router.put('/update')
async def update_user_info(
        user_data: UserUpdateRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    updated_user = await user_service.update_user_info(db, user, user_data)
    return response.success_response(message="更新用户信息成功", data=UserInfoResponse.model_validate(updated_user))


# 修改密码：认证依赖注入当前用户 -> 交给 service 校验并更新 -> 响应结果
@router.put('/password')
async def update_password(
        password_data: UserChangePasswordRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(get_current_user)
):
    await user_service.change_password(db, user, password_data.old_password, password_data.new_password)
    return response.success_response(message="更新密码成功")
