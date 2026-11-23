from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRegister(BaseModel):
    username: str
    password: str

# user_info 对应的类： 基础类 + Info 类（id, 用户名）
class UserInfoBase(BaseModel):
    # 用户信息基础数据模型
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=200, description="头像")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=255, description="简介")

class UserInfoResponse(UserInfoBase):
    id: int = Field(..., description="用户ID")
    username: str = Field(..., max_length=50, description="用户名")

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True, # 允许从 ORM 对象属性中取值
    )

# data 数据类型
class UserAuthData(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")
    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # alias / 字段名兼容
        from_attributes=True, # 允许从 ORM 对象属性中取值
    )

# 更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=200, description="头像")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=255, description="简介")
    phone: Optional[str] = Field(None, max_length=11, description="手机号")

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True, # 允许从 ORM 对象属性中取值
    )


class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., max_length=8, alias="oldPassword", description="旧密码")
    new_password: str = Field(..., max_length=8, alias="newPassword", description="新密码")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # 输入时同时接受驼峰别名与下划线字段名
    )

