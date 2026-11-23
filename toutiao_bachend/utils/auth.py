from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from services import auth


# 认证依赖：解析 Authorization 头 -> 校验 token（业务规则在 service 层）-> 返回当前用户
async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db: AsyncSession = Depends(get_db)):
    token = authorization.replace("Bearer ", "")
    user = await auth.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
